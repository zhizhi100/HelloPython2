# encoding: utf-8
'''
Created on 2015年11月15日

@author: ZhongPing
'''
import tornado.web
import json
from gt.gtcore.nsr import Nsr,UNsr
import gt.gtcore.sysinfo as g3sys 
from gt.gtcore import nsr
from gt.gtcore.env import Gtenv
        
class AjaxHandler(tornado.web.RequestHandler):
    def work(self):
        succ = True
        msg = ''
        data = {}
        return succ,msg,data
    
    def _work(self):
        self.uid = self.get_argument("uid", "")
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
        size = self.get_argument('pagesize', 200)
        p={}
        p['name']=nsrmc
        p['page']=page
        p['pagesize']=size
        n = UNsr(self.uid)
        succ,data = n.getmany(p)
        if succ:
            return succ,'',data
        else:
            return succ,data,None
        
class Querytrace(AjaxHandler):
    def work(self):
        n = UNsr(self.uid)
        succ,data = n.getlogs()
        if succ:
            return succ,'',data
        else:
            return succ,data,None
        
class G3info(AjaxHandler):
    def work(self):
        g3 = g3sys.Sysinfo();
        act = self.get_argument('act', 'get')
        if act == 'get':
            key = self.get_argument('key', 'key')
            val = g3.get(key)
            if val is None:
                return False,'',''
            else:
                return True,'',val
            
        if act == 'set':
            key = self.get_argument('key', 'key')
            val = self.get_argument('val', 'val')
            env = Gtenv("")
            dt = json.loads(val)
            #env.uid = dt["uid"]
            env.setuid(dt["uid"])
            #print env.uid     
            succ,msg = g3.set(key,val)
            return succ,msg,''

class SaveRemoteQuery(AjaxHandler):
    def work(self):
        nsrs = self.get_argument('nsrs')
        #print nsrs
        infos = json.loads(nsrs)
        infos = json.loads(infos)
        cols_str = 'ygznsrlxDm|hsfsDm|wjcyrs|djrq|whsyjsfjfxxdjbz|bsrdzxx|djzclxDm|cwfzrsfzjhm|gdghlxDm|fddbrdzxx|zcdz|nsrztDm|zzjglxDm|nsrzgswjgxxList|zgswjmc|shxydm|scjydlxdh|scjyqxq|fddbrxm|jyfw|scjyqxz|bsrsfzjhm|zzlxDm|cwfzrsfzjzlDm|wztzbl|zcdzxzqhszDm|djxh|zcdzxzqhszmc|bsrsfzjzlDm|swdlrmc|zczb|fddbryddh|hymc|fddbrsfzjlxmc|fddbrgddh|kjzdzzDm|hjszd|scjydz|fddbrsfzjhm|swdlrlxdh|jdxzDm|wz|gykglxDm|pzsljgDm|scjydyzbm|bzfsDm|kqccsztdjbz|zgswjg|cwfzrdzxx|tzze|hyDm|zfjglxDm|fddbrsfzjlxDm|dwlsgxDm|djjgDm|zzhm|gdgrs|gytzbl|lrrq|pzsljglxDm|lsswdjyxqz|wcjyhdssglzmbh|cyrs|lsswdjyxqq|zzjgDm|bsryddh|ggrs|cwfzrgddh|swdlrnsrsbh|bsrxm|kzztdjlxmc|jdxzmc|ssdabh|nsrmc|pzsljgmc|scjydzxzqhszmc|zrrtzbl|scjydzxzqhszDm|zzsqylxDm|hhrs|lrrDm|zgswskfjDm|bsrgddh|kyslrq|kzztdjlxDm|zcdyzbm|zgswskfjmc|nsrfyhyxxList|ssglyDm|nsrbm|pzzmhwjh|zgswjDm|zsxmcxbzDm|cwfzryddh|swdjblbz|djzclxmc|nsrztmc|zzsjylb|yhsjnfsDm|gdslxDm|ssglymc|zcdlxdh|fjmqybz|swdlrdzxx|gjhdqszDm|cwfzrxm|logtime|nsrsbh'
        cols = cols_str.split('|')
        for j in infos:
            for c in cols:
                if not j.has_key(c):
                    j[c]=""                       
        n = UNsr(self.uid)
        n.savemany(infos)
        return True,'',''
           
if __name__ == '__main__':
    n = Nsr()
    p = {}
    p['name']='长沙'
    p['pagesize']=3
    p['page']=1
    a,b = n.getmany(p)
    print b
        
