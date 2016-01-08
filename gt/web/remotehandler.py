# encoding: utf-8
'''
Created on 2015年12月4日

@author: zhongping
'''
import logging
import tornado.web
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPClient
from tornado.web import HTTPError, asynchronous

class RemoteQuery(tornado.web.RequestHandler):
    def _on_succ(self,txt):
        self.write(txt)
    
    def _work(self):
        #self.write('this job is just for test')
        headers = dict(self.request.headers)
        #if headers.has_key('url'):
        #    headers['url']='download.sword?ctrl=CX302ZxcxCtrl_exequery&sjymc=ysctycx_hnlthxcx_g'
        url = 'http://ysctycx.hnds.tax.cn:7001/download.sword?ctrl=CX302ZxcxCtrl_exequery&sjymc=ysctycx_hnlthxcx_g'
        body=self.request.body
        req = HTTPRequest(url=url,method='POST',headers=headers,body=body)
        clt = HTTPClient()
        txt = ''
        try:
            txt = clt.fetch(req)
            print txt.body
            self.write(txt.body)     
        except Exception as e:
            print str(e)
        clt.close()
          
        
    def get(self):
        self._work()
        
    def post(self):
        self._work()    

if __name__ == '__main__':
    pass