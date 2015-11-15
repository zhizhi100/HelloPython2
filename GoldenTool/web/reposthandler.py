# encoding: utf-8
'''
Created on 2015年11月11日

@author: ZhongPing
'''
import logging
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
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
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
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            #print response.body
            if response.body:
                self.write(response.body)
            self._on_success(response)
            self.finish()
            
    def _on_success(self,response):
        pass
    
class Test(Repost):
    def _on_success(self,response):
        if response.body:
            print response.body
            
class Querynsr(Repost):
    def _on_success(self,response):
        if response.body:
            pass