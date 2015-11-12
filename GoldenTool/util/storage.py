# encoding: utf-8
'''
Created on 2015年11月12日

@author: ZhongPing
'''
import os
import bsddb

class Gtqueue(object):
    '''
    NSR queue
    '''
    _path = ''
    _file = ''
    _length = 0

    def __init__(self, p, f, l=50):
        '''
        Constructor
        '''
        self._path = p
        self._file = p+'.'+f
        self._length = l
    
    def _prepare(self):
        try:
            os.mkdir(self._path)
        except:
            pass    
        dbenv = bsddb.db.DBEnv()
        dbenv.open(self._path, bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL)
        d = bsddb.db.DB(dbenv)
        # queue必须要设置一个value的长度，它的value是定长的
        d.set_re_len(20)
        d.open(self._file, bsddb.db.DB_QUEUE, bsddb.db.DB_CREATE, 0666)
        return dbenv,d
    
    def update(self,key,val):
        dbenv,d = self._prepare()
        d.put(key,val)
        d.sync()
        d.close()
        dbenv.close()
    
    #it's faild,you can not append value with specied key
    def append(self,key,val):
        dbenv,d = self._prepare()
        if d.has_key(key): d.delete(key)
        #d.put(key,val,flags=2)=d.append(val)
        d.put(key,val)
        d.sync()
        d.close()
        dbenv.close()
        
    def get(self,key):
        dbenv,d = self._prepare()
        val = d.get(key)
        d.sync()
        d.close()
        dbenv.close()
        return val
    
    def list(self):
        dbenv,d = self._prepare()
        items = d.items()
        d.sync()
        d.close()
        dbenv.close()
        return items
 
if __name__ == '__main__':
    q = Gtqueue('.','gqtest.db',20)
    q.update(100,'val1')
    q.update(200,'val2')
    q.update(300,'val3')
    
    for k,v in q.list():
        print k,v
    
    print q.get(200)
    q.append(101,'val:101')
    for k,v in q.list():
        print k,v    
    