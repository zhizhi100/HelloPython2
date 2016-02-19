# encoding: utf-8
'''
Created on 2016年1月25日

@author: ZhongPing
'''
from gt.util.gtdao import Dao
import env
import json

class Freq(object):
    _sql = '''CREATE TABLE `freq` (
                          `path` varchar(200) NOT NULL,
                          `times` int(11) DEFAULT 1,
                          `datas` varchar(2000) DEFAULT NULL,
                           PRIMARY KEY (`path`)
                        )'''
    
    def __init__(self,uid):
        sql = (self._sql,)
        myenv = env.Gtenv("")
        path = myenv.getpath()
        self.dao = Dao(path + "/" + uid + '_freq.db',sql)
        
    def _isnew(self,path):
        sql = 'select times from freq where path=?'
        succ,msg,r = self.dao.get(sql, [path])
        if r is None or len(r)==0:
            return True
        else:
            return False
        
    def save(self,datas):
        inserts = []
        updates = []
        for info in datas:
            path = info['path']
            data = []
            data.append(info['times'])
            data.append(json.dumps(info))
            data.append(info['path'])            
            if self._isnew(path):
                inserts.append(data)
            else:
                updates.append(data)
                
        if len(inserts)>0:
            sql = 'INSERT INTO freq(times,datas,path)values(?,?,?)'
            succ,msg = self.dao.savemany(sql, inserts)
            #return succ,msg
        
        if len(updates)>0:
            sql = 'UPDATE freq set times=?,datas=? where path=?'
            succ,msg = self.dao.savemany(sql, updates)
            #return succ,msg
        return True,''
            
    def query(self):
        sql = 'select datas from freq order by times desc limit 20'
        succ,msg,res = self.dao.getmany(sql)
        if succ:
            return True,res
        else:
            return False,msg

if __name__ == '__main__':
    l = 'E://workspace//gt//gt'
    myenv = env.Gtenv(l)
    f = Freq('24300001360')
    datas = []
    d = {}
    d['path']='http://yschxqd.hnds.tax.cn:7001/sword?ctrl=SB175FxmtysbCtrl_initView'
    d['times']=60
    d['data']='abcd'
    datas.append(d)
    f.save(datas)
    print f.query()