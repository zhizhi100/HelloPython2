# encoding: utf-8
'''
Created on 2015年11月3日

@author: ZhongPing
'''
import os
import re
from _random import Random
print os.path.abspath(__file__)

class A():
    def printname(self):
        t = self.getname()
        print(t)
        
    def getname(self):
        return 'my name is a'
    
class A1(A):
    def getname(self):
        return 'I\'m a1'
'''    
a = A()
a1 = A1()
a.printname()
a1.printname()
'''
   
import bsddb

def queque():    
    filepath = "."
    home = filepath
    filename = filepath + '/'+"testqueue.db"
    try:
        os.mkdir(filepath)
    except:
        pass    
    dbenv = bsddb.db.DBEnv()
    dbenv.open(home, bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL)
    d = bsddb.db.DB(dbenv)
    # queue必须要设置一个value的长度，它的value是定长的
    d.set_re_len(20)
    d.open(filename, bsddb.db.DB_QUEUE, bsddb.db.DB_CREATE, 0666)
    # 它的key必须是数字
    d.put(1, 'zhaowei')
    for i in range(1,100):
        d.put(i,'val is :'+str(i))
    for (k,v) in d.items()[::-1]:
        print k,v
    
    d.close()
    dbenv.close()
    
def getqueue():
    filepath = "."
    filename = filepath + '/'+"testqueue.db"
    '''
    d= bsddb.open(filename, bsddb.db.DB_QUEUE, bsddb.db.DB_CREATE, 0666)
    print d.items()

    d.close()
    '''

def btree():
    d = bsddb.btopen('btree.db', 'c')
    for i in range(1,100):
        d[i] ='val is :'+str(i)
    d.sync()
    for (k,v) in d.items()[::-1]:
        print k,v

    d.close()
        
#queque()
#getqueue()
#btree()

def retest():
    a = 'http://------/_gtool_/hello.js'
    b = '^http.*?_gtool_.*'
    d = '^http.*?_gtool_'
    if re.match(b, a):
        print 1
    else:
        print 0
    c = re.sub(d, 'http://localhost:80/static', a)
    print a
    print c
    
    a = 'http://127.0.0.1/_gtool_query_/querynsr'
    b = '^http.*?_gtool_query_.*'
    d = '^http.*?_gtool_query_'
    if re.match(b, a):
        print 1
    else:
        print 0
    c = re.sub(d, 'http://127.0.0.1:80', a)
    print a
    print c    
        
#retest()

id ='BFEBFBFF000306A9'
import hashlib   

m2 = hashlib.md5()   
m2.update(id)   
print m2.hexdigest()
print m2.digest()   

import datetime
import random
print datetime.datetime.now()
for i in range(1,1000):
    k = random.randint(0,100)
print datetime.datetime.now()

import ConfigParser
cf = ConfigParser.ConfigParser()
path = '.'
cf.read(path + "/service.ini")
logfile = cf.get("log","local")
print logfile
