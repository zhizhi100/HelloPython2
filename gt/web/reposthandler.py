# encoding: utf-8
'''
Created on 2015年11月11日

@author: ZhongPing
'''
import os
import json
import logging
import time
import threading
import tornado.web
import tornado.httpclient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tornado.web import HTTPError, asynchronous

class Repost(tornado.web.RequestHandler):
    def get(self):
        self.write("just for test") 
        
    @asynchronous
    def post(self):
        headers = dict(self.request.headers)
        url = ''
        if headers.has_key('Gtool_url'):
            url = headers['Gtool_url']
            del headers['Gtool_url']
        else:
            raise HTTPError(500)
        #print headers
        #print self.request.body 
        try:
            logging.info('to fecth url:%s',url)
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
            logging.info('finished in fecthing url:%s',url)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)
                       
    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location", "Content-Disposition"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            
            '''
            for k,v in response.headers.items():
                self.set_header(k, v)
            '''
            #print response.body
            if response.body:
                self.write(response.body)
            self.finish()
            self._on_success(response)
            
    def _on_success(self,response):
        pass
    
class Test(Repost):
    def _on_success(self,response):
        if response.body:
            print response.body
            
class Loadnsr(Repost):
    def _on_success(self,response):
        if response.body:
            pass
        
class GetNsrDetail(Repost):
    def _on_success(self, response):
        if response.body:
            from gt.gtcore.nsr import Nsr
            nsr = Nsr()
            info = nsr.getxxfromquery(response.body)
            nsr.savetrace(info)
            nsr.save(info)
        
class Downloader(Repost):
    def test(self):
        from time import ctime,sleep
        sleep(6)
    
    def newjob(self,target):
        t = threading.Thread(target=target)
        t.setDaemon(True)
        t.start()
    
    def storensr(self,txt):
        r = int(time.time())
        f = 'tmp'+str(r)+'.data'
        fo = open(f,'w')
        try:
            fo.write(txt)
        finally:
            fo.close()
        AsyncHTTPClient().fetch(
            HTTPRequest(url='http://127.0.0.1:8001/importnsr?file='+f,
                        method="GET",
                        follow_redirects=False),
            None)
    
    def isdownloadnsrlist(self,data):
        isnsr = False
        if data is not None: #is 税务登记信息查询
            data = json.loads(data)
            if data.has_key('data'):
                data = data['data']
                if len(data)==1:
                    data = data[0]
                    if data.has_key('value'):
                        data = data['value']
                        data = json.loads(data)
                        data = data['sqlmc']
                        if data==u'\u7a0e\u52a1\u767b\u8bb0\u4fe1\u606f\u67e5\u8be2': #税务登记信息查询
                            isnsr = True       
        return isnsr
    
    def _on_success(self,response):
        if response.body:
            data = self.get_argument('postData',None)
            if self.isdownloadnsrlist(data):
                self.storensr(response.body)
                #self.newjob(self.storensr(response.body))
                #self.newjob(self.test())
                #logging.info('to new thread deal with database')
                #t = threading.Thread(target=self.storensr(response.body))
                #t.setDaemon(True)
                #t.start()

        