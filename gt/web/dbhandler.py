# encoding: utf-8
'''
Created on 2015年11月15日

@author: ZhongPing
'''
import tornado.web
import json
from gt.gtcore.nsr import Nsr
        
class AjaxHandler(tornado.web.RequestHandler):
    def work(self):
        succ = True
        msg = ''
        data = {}
        return succ,msg,data
    
    def _work(self):
        succ,msg,data = self.work()
        j = {}
        if succ:
            j['status']='1'
        else:
            j['status']='0'
        j['message']=msg
        j['data']=data
        self.write(json.dumps(j))
    
    def get(self):
        self._work()
        
    def post(self):
        self._work()
        
class Querynsr(AjaxHandler):
    def work(self):
        nsrmc=self.get_argument('name')
        if len(nsrmc) == 0:
            return False,'缺少关键参数！',None
        page = self.get_argument('page',1)
        size = self.get_argument('pagesize', 50)
        p={}
        p['name']=nsrmc
        p['page']=page
        p['pagesize']=size
        n = Nsr()
        succ,data = n.getmany(p)
        if succ:
            return succ,'',data
        else:
            return succ,data,None
           
if __name__ == '__main__':
    n = Nsr()
    p = {}
    p['name']='长沙'
    p['pagesize']=3
    p['page']=1
    a,b = n.getmany(p)
    print b
        
