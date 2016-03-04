# encoding: utf-8
'''
Created on 2015年11月13日

@author: ZhongPing
'''
import sqlite3
import os

class Dao(object):

    def __init__(self,path='gtool.db',initsqllist='',name='',*args,**kwargs):  
        self.name = name  
        self.path = path #数据库连接参数  
        db_path = self.path[:self.path.rfind(os.sep)]  
        if not os.path.exists(db_path):  
            os.makedirs(db_path)
        if not os.path.isfile(path):
            for i in initsqllist:
                self.define(i)
    
    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.text_factory = str
        return conn
        
    def close_conn(self,conn=None):
        conn.close()
        
    def close_cu(self,cu):
        try:
            if cu is not None:
                cu.close()
        finally:
            if cu is not None:
                cu.close()
                
    def close(self,conn,cu):
        self.close_cu(cu)
        self.close_conn(conn)
        
    def get_cursor(self,conn=None):
        if conn is not None:
            return conn.cursor()
        else:
            return None
        
    def _exec(self,sql,trans,data):
        if sql is not None and sql != '':
            try:
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                if data is not None:
                    d = tuple(data)
                    cu.execute(sql,d)
                else:
                    cu.execute(sql)
                if trans:conn.commit()
                self.close(conn, cu)
                return True,''
            except sqlite3.Error,e: 
                return False,'执行SQL语句失败！\nSQL语句:'+sql+'\n错误信息：'+e.args[0] 
        else:
            return False,'无效的SQL语句'        
    
    def define(self,sql,datalist=None):
        return self._exec(sql=sql,trans=True,data=datalist)
        
    def save(self,sql,datalist=None):
        return self._exec(sql=sql,trans=True, data=datalist)
    
    def savemany(self,sql,datamultilist=None,count=20):
        if count is None or count < 0:count=5
        if sql is not None and sql != '':
            try:
                conn = self.get_conn()
                cu = self.get_cursor(conn)
                if datamultilist is not None:
                    k = 0
                    for i in datamultilist:
                        k = k + 1
                        d = tuple(i)
                        cu.execute(sql,d)
                        if k % count == 0:
                            conn.commit()
                else:
                    cu.execute(sql)
                conn.commit()
                self.close(conn, cu)
                return True,''
            except sqlite3.Error,e: 
                return False,'执行SQL语句失败！\nSQL语句:'+sql+'\n错误信息：'+e.args[0] 
        else:
            return False,'无效的SQL语句'          
            
    def _query(self,sql,many,data):
        if sql is not None and sql != '':
            try:
                conn = self.get_conn()
                if data is not None:
                    d = tuple(data)
                    cu = conn.execute(sql,d)
                else:
                    cu = conn.execute(sql)
                if many:
                    res = cu.fetchall()
                else:
                    res = cu.fetchone()
                self.close(conn, cu)
                return True,'',res
            except sqlite3.Error,e: 
                return False,'执行SQL语句失败！\nSQL语句:'+sql+'\n错误信息：'+e.args[0],None
        else:
            return False,'无效的SQL语句',None
        
    def get(self,sql,datalist=None):
        return self._query(sql=sql, many=False,data=datalist)
        
    def getmany(self,sql,datalist=None):
        return self._query(sql=sql, many=True,data=datalist)
    
    def put(self):
        #to be finished
        #chaeck data before add,add data if not exists
        pass
        
    def putmany(self):
        #to be finished
        #check data before add,add data if not exists
        pass
    
    def saveobject(self):
        #to be finished
        #generate sql and execute,like ormap/thinkphp
        pass
    
class FileDAO(object):
    dao = None
    def __init__(self,title):
        path = title+'_files.db'
        sql = '''CREATE TABLE `files` (
                          `id` INTEGER PRIMARY KEY,
                          `name` varchar(255) NOT NULL,
                          `path` varchar(2048) NOT NULL,
                          `isfile` int(1) DEFAULT NULL,
                          `mtime` TIMESTAMP default (datetime('now', 'localtime')), 
                          `parent` varchar(2048) DEFAULT NULL,
                          `hotrank` int(11) DEFAULT NULL
                        )'''
        sqlb = '''CREATE TABLE `tmpfiles` (
                          `id` INTEGER PRIMARY KEY,
                          `name` varchar(255) NOT NULL,
                          `path` varchar(2048) NOT NULL,
                          `isfile` int(1) DEFAULT NULL,
                          `mtime` TIMESTAMP default (datetime('now', 'localtime')), 
                          `parent` varchar(2048) DEFAULT NULL,
                          `hotrank` int(11) DEFAULT NULL
                        )'''
        sqlc = '''CREATE TABLE `newfilejobs` (
                          `id` INTEGER PRIMARY KEY,
                          `name` varchar(255) NOT NULL,
                          `path` varchar(2048) NOT NULL,
                          `isfile` int(1) DEFAULT NULL,
                          `mtime` TIMESTAMP default (datetime('now', 'localtime')), 
                          `parent` varchar(2048) DEFAULT NULL,
                          `operation` varchar(20) DEFAULT NULL
                        )'''
        sqllist = {sql,sqlb,sqlc}
        self.dao = Dao(path=path,initsqllist=sqllist)
    
    def addfile(self,afile):
        sql = '''INSERT INTO `files`(`name`,`path`,`isfile`,`mtime`,`parent`) 
                VALUES (?,?,?,?,?)
                '''
        list = {afile.name,afile.path,afile.isfile,afile.mtime,afile.parent}
        self.dao.save(sql, list)
        
    def addfiles(self,files,curpath = None):
        fs = []
        for afile in files:
            t = (afile.name,afile.path,afile.isfile,afile.mtime,afile.parent)
            fs.append(t)
        sql = 'delete from tmpfiles'
        self.dao.define(sql)
        sql = '''INSERT INTO `tmpfiles`(`name`,`path`,`isfile`,`mtime`,`parent`) 
                VALUES (?,?,?,?,?)
                '''
        self.dao.savemany(sql, fs, 100)
        #new files
        sql = '''insert into newfilejobs(`name`,`path`,`isfile`,`mtime`,`parent`,`operation`) 
                    select a.name,a.path,a.isfile,a.mtime,a.parent,'new' 
                    from tmpfiles a
                    where not exists(select 1 from files b where b.path=a.path )
                '''
        self.dao.define(sql)
        #modified files
        sql = '''insert into newfilejobs(`name`,`path`,`isfile`,`mtime`,`parent`,`operation`) 
                    select a.name,a.path,a.isfile,a.mtime,a.parent,'modified' from files b,tmpfiles a 
                        where a.path=b.path and a.mtime<>b.mtime
                '''
        self.dao.define(sql)
        #deleted files
        if curpath is not None:
            #add job
            sql = '''insert into newfilejobs(`name`,`path`,`isfile`,`mtime`,`parent`,`operation`) 
                        select a.name,a.path,a.isfile,a.mtime,a.parent,'deleted' from files a 
                            where not exists(select 1 from tmpfiles b where b.path=a.path ) and a.parent=?
                    ''' 
            self.dao.define(sql,(curpath,))
            #delete the files record
            sql = '''delete from files a 
                            where not exists(select 1 from tmpfiles b where b.path=a.path ) and a.parent=?
                    ''' 
            self.dao.define(sql,(curpath,))            
        #modified files        
        sql = '''update files set mtime=(select c.mtime from ( 
                    select a.path,b.mtime from files a,tmpfiles b 
                        where a.path=b.path and a.mtime<>b.mtime) c
                where files.path=c.path
                '''
        self.dao.define(sql)
        #new files
        sql = '''insert into files(`name`,`path`,`isfile`,`mtime`,`parent`) 
                    select a.name,a.path,a.isfile,a.mtime,a.parent from tmpfiles a 
                        where not exists ( select 1 from files b where b.path=a.path )
                '''
        self.dao.define(sql)
        
    def gethotdir(self,fromtimestamp):
        sql = 'SELECT `name`,`path`,`isfile`,`mtime`,`id` FROM `files` WHERE `isfile`=0 and `mtime`>?'
        (succ,msg,row) = self.dao.getmany(sql, (fromtimestamp,))
        return row
        
    def getfile(self,fid):
        sql = 'SELECT `name`,`path`,`isfile`,`mtime`,`parent` FROM `files` WHERE `id`=?'
        (succ,msg,row) = self.dao.get(sql, (fid,))
        return row
    
    def getchildfiles(self,fid):
        sql = 'SELECT `name`,`path`,`isfile`,`mtime`,`id` FROM `files` WHERE `parent`=?'
        (succ,msg,row) = self.dao.getmany(sql, (fid,))
        return row
    
    def istravled(self):
        sql = 'SELECT `id` FROM `files` limit 1'
        (succ,msg,row) = self.dao.get(sql)
        if row is None:
            return False
        else:
            return True
           
        
def test():
    k = 8
    i = 2
    print k % i
    if k % i == 0:print 10
    d = Dao('test.db')
    #sql = 'CREATE TABLE tbl_test(i_index INTEGER PRIMARY KEY, sc_name VARCHAR(32));'
    #d.define(sql)
    sql = "INSERT INTO tbl_test(sc_name) values('abc');" 
    d.save(sql)
    sql = "INSERT INTO tbl_test(sc_name) values(?);" 
    data = 'one'
    print d.save(sql, data)
    data = ['one','tow','three','four']
    print d.savemany(sql, data,2)
    print d.savemany(sql, data,5)
    sql = "select 1 from tbl_test where i_index=?;"
    succ,msg,r = d.getmany(sql, '100000')
    if len(r)>0:print 'has it'
    else:
        print 'do not has it'
    '''
    k = r[2]
    k = k[0]
    print k[0]
    '''
        
def testb():
    fdao = FileDAO('testa')
    fdao.istravled()
    import time
    now = int(time.time())
    fromtimestamp = now - 20 * 365 * 24 * 60 * 60
    dirs = fdao.gethotdir(fromtimestamp)
    for dir in dirs:
        print dir
        print dir[1]
    
if __name__ == '__main__':
    #test()
    testb()    
    