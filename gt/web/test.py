# encoding: utf-8
'''
Created on 2015年11月15日

@author: ZhongPing
'''
from GoldenTool.gtcore.regist import Nsr

if __name__ == '__main__':
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
    
    conn = sqlite3.connect('test.db')
    print "Opened database successfully";
    
    cursor = conn.execute("SELECT *  from gt_nsr")
    
    print "Operation done successfully";
    conn.close()