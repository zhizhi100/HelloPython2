# encoding: utf-8
'''
Created on 2015年12月8日

@author: ZhongPing
'''
import base64
import gt.util.gtdao as mydao

class Sysinfo(object):
    
    dao = None
    getsql = 'select value from g3server where param=?'
    setsql = 'update g3server set value=? where param=?'
    
    def __init__(self):
        
        self.dao = mydao.Dao(path="HTTPD.dll",initsqls='')
        
    def set(self,key,val):
        succ,msg = self.dao.save(self.setsql, [val,key])
        return succ,msg
    
    def get(self,key):
        succ,msg,res = self.dao.get(self.getsql, [key])
        if succ:
            if res is None or len(res)!=1:
                return None
            else:
                return  res[0]
        else:
            return None
        
if __name__ == '__main__':
    sys = Sysinfo();
    print sys.set('servertime', 'val2')
    print sys.get('servertime')
    pass