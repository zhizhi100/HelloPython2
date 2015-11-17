# encoding: utf-8
'''
Created on 2015年11月12日

@author: ZhongPing
'''
import json
import datetime
from gt.util.gtdao import Dao
from copy import copy,deepcopy

class Nsr(object):
    '''
    classdocs
    '''
    info = {}#dict,like that{'nsrsbh':'23423',''....}
    dao = None
    cols = []

    def __init__(self):
        '''
        Constructor
        '''
        sql = self._create_tb_sql()
        self.dao = Dao('gtnsr.db',sql)
        #cols_str pk is nsrsbh,must be end with nsrsbh
        cols_str = 'ygznsrlxDm|hsfsDm|wjcyrs|djrq|whsyjsfjfxxdjbz|bsrdzxx|djzclxDm|cwfzrsfzjhm|gdghlxDm|fddbrdzxx|zcdz|nsrztDm|zzjglxDm|nsrzgswjgxxList|zgswjmc|shxydm|scjydlxdh|scjyqxq|fddbrxm|jyfw|scjyqxz|bsrsfzjhm|zzlxDm|cwfzrsfzjzlDm|wztzbl|zcdzxzqhszDm|djxh|zcdzxzqhszmc|bsrsfzjzlDm|swdlrmc|zczb|fddbryddh|hymc|fddbrsfzjlxmc|fddbrgddh|kjzdzzDm|hjszd|scjydz|fddbrsfzjhm|swdlrlxdh|jdxzDm|wz|gykglxDm|pzsljgDm|scjydyzbm|bzfsDm|kqccsztdjbz|zgswjg|cwfzrdzxx|tzze|hyDm|zfjglxDm|fddbrsfzjlxDm|dwlsgxDm|djjgDm|zzhm|gdgrs|gytzbl|lrrq|pzsljglxDm|lsswdjyxqz|wcjyhdssglzmbh|cyrs|lsswdjyxqq|zzjgDm|bsryddh|ggrs|cwfzrgddh|swdlrnsrsbh|bsrxm|kzztdjlxmc|jdxzmc|ssdabh|nsrmc|pzsljgmc|scjydzxzqhszmc|zrrtzbl|scjydzxzqhszDm|zzsqylxDm|hhrs|lrrDm|zgswskfjDm|bsrgddh|kyslrq|kzztdjlxDm|zcdyzbm|zgswskfjmc|nsrfyhyxxList|ssglyDm|nsrbm|pzzmhwjh|zgswjDm|zsxmcxbzDm|cwfzryddh|swdjblbz|djzclxmc|nsrztmc|zzsjylb|yhsjnfsDm|gdslxDm|ssglymc|zcdlxdh|fjmqybz|swdlrdzxx|gjhdqszDm|cwfzrxm|logtime|nsrsbh'
        self.cols = cols_str.split('|')
        for i in self.cols:
            self.info[i]=''
        #print self.cols
        
    def _info(self,col):
        v = self.info
        if v.has_key(col):
            return v[col]
        else:
            return None
        
    def getinfo(self):
        return self.info
    
    def getxxfromquery(self,js):
        try:
            d = json.loads(js)
            d = d['data'][1]['trs'][0]['tds']
            self.info.clear()
            #self.info['nsrsbh']=d['nsrsbh']['value']
            #print self.cols
            for i in self.cols:
                if d.has_key(i):
                    self.info[i]= d[i]['value']
        finally:
            return self.info
      
    def _isexsits(self,dm):
        sql = 'select 1 from gt_nsr where nsrsbh=?'
        succ,msg,r = self.dao.get(sql, dm)
        if r is None or len(r)==0:
            return False
        else:
            return True
        
    def _isloged(self,dm):
        sql = 'select 1 from gt_nsr_access where nsrsbh=?'
        succ,msg,r = self.dao.get(sql, dm)
        if r is None or len(r)==0:
            return False
        else:
            return True
             
    def getxxfromdao(self,dm):
        sql = 'select '+ ",".join(self.cols) +' from gt_nsr where nsrsbh=?'
        succ,msg,res = self.dao.get(sql, dm)
        if succ:
            self.info.clear()
            k = 0
            for i in self.cols:
                self.info[i]= res[k]
                k = k + 1
            return self.info   
        else:
            return None
        
    def getlogs(self):
        sql = 'select nsrmc,scjydz,zgswskfjmc,ssglymc,nsrsbh,logtime from gt_nsr_access order by logtime desc limit 100'
        succ,msg,res = self.dao.getmany(sql)
        if succ:
            l = []
            for r in res:
                info = {}
                info['nsrmc'] = r[0]
                info['scjydz'] = r[1]
                info['zgswskfjmc'] = r[2]
                info['ssglymc'] = r[3]
                info['nsrsbh'] = r[4]
                info['logtime'] = r[5]
                l.append(info)
            return True,l
        else:
            return False,msg
        
    def getmany(self,params):
        sql = 'select '+ ",".join(self.cols) +' from gt_nsr where 1'
        data = []
        if params.has_key('name'):
            #print params['name']
            sql=sql+' and nsrmc like ? '
            data.append('%'+params['name']+'%')
        sql = sql + ' order by zgswskfjmc,ssglymc,nsrmc'            
        if params.has_key('pagesize'):
            sql = sql+' limit ?'
            data.append(params['pagesize'])
        if params.has_key('page'):
            sql = sql+ ' OFFSET ?'
            j = params['page'] - 1
            data.append(j)
        succ,msg,res = self.dao.getmany(sql, data)
        if succ:
            l = []
            for r in res:
                info = {}
                k = 0
                for i in self.cols:
                    info[i]= r[k]
                    k = k + 1                
                l.append(info)
            return True,l
        else:
            return False,msg
        
    def needsave(self,dm):
        sql = 'select date(logtime) from gt_nsr where nsrsbh=?'
        succ,msg,r = self.dao.get(sql, dm)
        if r is None or len(r)==0:
            return True
        else:
            logtime = r[0]
            t = datetime.datetime.now() - datetime.datetime.strptime(logtime, '%Y-%m-%d')
            if t.days > 0:
                return True
            else:
                return False  
      
    def save(self,info):
        dm = self._info('nsrsbh')
        needsave = self.needsave(dm)
        if not needsave:return None
        isnew = not self._isexsits(dm)
        reps = '?'
        k = 2 #do not need logtime and nsrsbh
        j = len(self.cols)
        while k<j:
            reps = reps+',?'
            k = k + 1
        if isnew:
            s = ",".join(self.cols)
            s = s.replace(',logtime', '')
            sql = 'INSERT INTO gt_nsr('+s+")values("+reps+")"
        else:
            s = "=?,".join(self.cols)
            #print s
            s = s.replace(',logtime=?,nsrsbh', '')
            sql = "UPDATE gt_nsr set logtime=datetime('now', 'localtime'),"+s+' WHERE nsrsbh=?'
        data = self._getinfodata(info)
        #print data
        return self.dao.save(sql, data)
    
    def savemany(self,infos):
        for info in infos:
            self.save(info)
    
    def savetrace(self,info):
        dm = self._info('nsrsbh')
        isnew = not self._isloged(dm)
        if isnew: #primary key get the last position
            sql = 'INSERT INTO gt_nsr_access(nsrmc,scjydz,zgswskfjmc,ssglymc,nsrsbh)values(?,?,?,?,?)'
        else:
            sql = '''UPDATE gt_nsr_access set nsrmc=?,scjydz=?,zgswskfjmc=?,ssglymc=?,
                     logtime=datetime('now', 'localtime') where nsrsbh=?'''
        data = []
        data.append(info['nsrmc'])
        data.append(info['scjydz'])
        data.append(info['zgswskfjmc'])
        data.append(info['ssglymc'])
        data.append(info['nsrsbh'])
        return self.dao.save(sql, data)
    
    def _getinfodata(self,info=None):
        if info is None:info=self.info
        data = []
        for k in self.cols:
            if k=='logtime':continue
            data.append(info[k])
        return data
      
    def _create_tb_sql(self):
        sql='''CREATE TABLE `student` (
                          `id` int(11) NOT NULL,
                          `name` varchar(20) NOT NULL,
                          `gender` varchar(4) DEFAULT NULL,
                          `age` int(11) DEFAULT NULL,
                          `address` varchar(200) DEFAULT NULL,
                          `phone` varchar(20) DEFAULT NULL,
                           PRIMARY KEY (`id`)
                        )'''
        sql = "CREATE TABLE IF NOT EXISTS gt_nsr(ygznsrlxDm varchar(50) DEFAULT NULL, hsfsDm varchar(50) DEFAULT NULL, wjcyrs varchar(50) DEFAULT NULL, djrq varchar(50) DEFAULT NULL, whsyjsfjfxxdjbz varchar(50) DEFAULT NULL, bsrdzxx varchar(50) DEFAULT NULL, djzclxDm varchar(50) DEFAULT NULL, cwfzrsfzjhm varchar(50) DEFAULT NULL, gdghlxDm varchar(50) DEFAULT NULL, fddbrdzxx varchar(50) DEFAULT NULL, zcdz varchar(500) DEFAULT NULL, nsrztDm varchar(50) DEFAULT NULL, zzjglxDm varchar(50) DEFAULT NULL, nsrzgswjgxxList varchar(1000) DEFAULT NULL, zgswjmc varchar(50) DEFAULT NULL, shxydm varchar(50) DEFAULT NULL, scjydlxdh varchar(50) DEFAULT NULL, scjyqxq varchar(50) DEFAULT NULL, fddbrxm varchar(50) DEFAULT NULL, jyfw varchar(1000) DEFAULT NULL, scjyqxz varchar(50) DEFAULT NULL, bsrsfzjhm varchar(50) DEFAULT NULL, zzlxDm varchar(50) DEFAULT NULL, cwfzrsfzjzlDm varchar(50) DEFAULT NULL, wztzbl varchar(50) DEFAULT NULL, zcdzxzqhszDm varchar(50) DEFAULT NULL, djxh varchar(50) DEFAULT NULL, zcdzxzqhszmc varchar(50) DEFAULT NULL, bsrsfzjzlDm varchar(50) DEFAULT NULL, swdlrmc varchar(50) DEFAULT NULL, zczb varchar(50) DEFAULT NULL, fddbryddh varchar(50) DEFAULT NULL, hymc varchar(50) DEFAULT NULL, fddbrsfzjlxmc varchar(50) DEFAULT NULL, fddbrgddh varchar(50) DEFAULT NULL, kjzdzzDm varchar(50) DEFAULT NULL, hjszd varchar(50) DEFAULT NULL, scjydz varchar(500) DEFAULT NULL, fddbrsfzjhm varchar(50) DEFAULT NULL, swdlrlxdh varchar(50) DEFAULT NULL, jdxzDm varchar(50) DEFAULT NULL, wz varchar(50) DEFAULT NULL, gykglxDm varchar(50) DEFAULT NULL, pzsljgDm varchar(50) DEFAULT NULL, scjydyzbm varchar(50) DEFAULT NULL, bzfsDm varchar(50) DEFAULT NULL, kqccsztdjbz varchar(50) DEFAULT NULL, zgswjg varchar(500) DEFAULT NULL, cwfzrdzxx varchar(50) DEFAULT NULL, tzze varchar(50) DEFAULT NULL, hyDm varchar(50) DEFAULT NULL, zfjglxDm varchar(50) DEFAULT NULL, fddbrsfzjlxDm varchar(50) DEFAULT NULL, dwlsgxDm varchar(50) DEFAULT NULL, djjgDm varchar(50) DEFAULT NULL, zzhm varchar(50) DEFAULT NULL, gdgrs varchar(50) DEFAULT NULL, gytzbl varchar(50) DEFAULT NULL, lrrq varchar(50) DEFAULT NULL, pzsljglxDm varchar(50) DEFAULT NULL, lsswdjyxqz varchar(50) DEFAULT NULL, wcjyhdssglzmbh varchar(50) DEFAULT NULL, cyrs varchar(50) DEFAULT NULL, lsswdjyxqq varchar(50) DEFAULT NULL, zzjgDm varchar(50) DEFAULT NULL, bsryddh varchar(50) DEFAULT NULL, ggrs varchar(50) DEFAULT NULL, cwfzrgddh varchar(50) DEFAULT NULL, swdlrnsrsbh varchar(50) DEFAULT NULL, bsrxm varchar(50) DEFAULT NULL, kzztdjlxmc varchar(50) DEFAULT NULL, jdxzmc varchar(50) DEFAULT NULL, ssdabh varchar(50) DEFAULT NULL, nsrmc varchar(500) DEFAULT NULL, pzsljgmc varchar(50) DEFAULT NULL, scjydzxzqhszmc varchar(50) DEFAULT NULL, zrrtzbl varchar(50) DEFAULT NULL, scjydzxzqhszDm varchar(50) DEFAULT NULL, zzsqylxDm varchar(50) DEFAULT NULL, nsrsbh varchar(50) DEFAULT NULL, hhrs varchar(50) DEFAULT NULL, lrrDm varchar(50) DEFAULT NULL, zgswskfjDm varchar(50) DEFAULT NULL, bsrgddh varchar(50) DEFAULT NULL, kyslrq varchar(50) DEFAULT NULL, kzztdjlxDm varchar(50) DEFAULT NULL, zcdyzbm varchar(50) DEFAULT NULL, zgswskfjmc varchar(50) DEFAULT NULL, nsrfyhyxxList varchar(50) DEFAULT NULL, ssglyDm varchar(50) DEFAULT NULL, nsrbm varchar(50) DEFAULT NULL, pzzmhwjh varchar(50) DEFAULT NULL, zgswjDm varchar(50) DEFAULT NULL, zsxmcxbzDm varchar(50) DEFAULT NULL, cwfzryddh varchar(50) DEFAULT NULL, swdjblbz varchar(50) DEFAULT NULL, djzclxmc varchar(50) DEFAULT NULL, nsrztmc varchar(50) DEFAULT NULL, zzsjylb varchar(50) DEFAULT NULL, yhsjnfsDm varchar(50) DEFAULT NULL, gdslxDm varchar(50) DEFAULT NULL, ssglymc varchar(50) DEFAULT NULL, zcdlxdh varchar(50) DEFAULT NULL, fjmqybz varchar(50) DEFAULT NULL, swdlrdzxx varchar(50) DEFAULT NULL, gjhdqszDm varchar(50) DEFAULT NULL, cwfzrxm varchar(50) DEFAULT NULL,logtime TIMESTAMP default (datetime('now', 'localtime')),  PRIMARY KEY (nsrsbh) );"
        sql2 = '''CREATE TABLE IF NOT EXISTS gt_nsr_access (
                    nsrsbh varchar(50) NOT NULL, 
                    nsrmc varchar(500) DEFAULT NULL, 
                    scjydz varchar(500) DEFAULT NULL, 
                    zgswskfjmc varchar(50) DEFAULT NULL, 
                    ssglymc varchar(50) DEFAULT NULL, 
                    logtime TIMESTAMP default (datetime('now', 'localtime')), 
                    PRIMARY KEY (nsrsbh)                    
                )'''
        sql3 = 'CREATE INDEX logtime_index ON gt_nsr_access(logtime)' 
        return {sql,sql2,sql3}
    
if __name__ == '__main__':
    '''
    f = open('nsrxx.txt')
    try:
        js = f.read()
    finally:
        f.close()
    '''
    n = Nsr()
    #r = nsr.getxxfromquery(js)
    #r = nsr.getxxfromdao('430111351684870')
    #nsr.save(r)
    #nsr.savetrace(r)
    p = {}
    p['name']='长沙'
    p['pagesize']=3
    p['page']=1
    a,b = n.getmany(p)
    print b
    #print "=?,".join(nsr.cols)
    #print n._info('nsrsbh')
    #print n._info('nsrmc')
    #d =  nsr.getxxfromdao('430111351684870')
    #print nsr
    '''
    r = nsr._getinfodata()
    for i in r:
        #print i
        pass
    #print r
    for k,v in r.items():
        #print k
        pass 
    for k in r:
        #print k
        pass
    '''
    #nsr = Nsr()
    #sql = nsr._create_tb_sql()
    #d = Dao('gtnsr.db',sql)
    #print d.define("drop table gt_nsr")
