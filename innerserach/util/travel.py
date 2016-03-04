# -*- coding: UTF8 -*-
'''
Created on 2016年2月23日

@author: ZhongPing
'''

from innerdao import FileDAO
from common import FileStruct
import ftplib
import os
import time
    
class Travesal(object):
    def __init__(self):
        pass
    def listfiles(self,path):
        return []
    def travel(self,path):
        return []

class FileTravesal(Travesal):
    def listfiles(self,path):
        files = []
        for i in os.listdir(path):
            f = os.path.join(path,i)
            finfo = os.stat(f)
            file = FileStruct()
            file.name = i
            file.path = f
            file.mtime = finfo.st_mtime  
            file.isfile = 0
            file.parent = path
            if os.path.isfile(f):
                file.isfile = 1
            files.append(file)
        return files
     
    def travel(self, path):
        files = []
        for root, dirs, filelist in os.walk(path):
            for dir in dirs:
                f = os.path.join(root,dir)
                finfo = os.stat(f)
                file = FileStruct()
                file.name = dir
                file.path = f
                file.mtime = finfo.st_mtime  
                file.isfile = 0
                file.parent = root  
                files.append(file)              
            for fn in filelist:
                f = os.path.join(root,fn)
                finfo = os.stat(f)
                file = FileStruct()
                file.name = fn
                file.path = f
                file.mtime = finfo.st_mtime  
                file.isfile = 1
                file.parent = root  
                files.append(file) 
        return files
    
class FTPTraversal(object):
    def __init__(self, host,uname,pwd):
        self.host = host
        self.uname = uname
        self.pwd = pwd
        self.ftp = None
        try:
            self.ftp = ftplib.FTP(host)
        except ftplib.error_perm: 
            #add log
            self.ftp = None   
        try:
            self.ftp.login(uname,pwd)
        except ftplib.error_perm:
            #print('登录失败')
            self.ftp.quit()
            self.ftp = None
            
    def __del__(self):
        if self.ftp is not None:
            self.ftp.quit() 
        
    def logout(self):
        if self.ftp is not None:
            self.ftp.quit()
        
    def download(self,FILE):
        if self.ftp is None:
            return None
        try:
            self.ftp.retrbinary('RETR %s' % FILE,open(FILE,'wb').write)
            #print('文件"%s"下载成功' % FILE)
        except ftplib.error_perm:
            #print('无法读取"%s"' % FILE)
            os.unlink(FILE)
                
    def listfiles(self):
        #return self.ftp.retrlines('LIST')
        self.ftp.set_pasv(False)
        self.ftp.cwd("/")
        return self.ftp.nlst() 
    
    def travel(self, path):
        print 'not finished!'
        return []
    
def list():
    path = u'D:\\phpStudy'
    trav = FileTravesal()
    fs = trav.listfiles(path)
    data = []
    for afile in fs:
        t = (afile.name,afile.path,afile.isfile,afile.mtime,afile.parent)
        data.append(t)
    dao = FileDAO('test')
    dao.addfiles(data,path)
    
def travel():
    path = u'D:\\phpStudy'
    trav = FileTravesal()
    fs = trav.travel(path)
    data = []
    for afile in fs:
        t = (afile.name,afile.path,afile.isfile,afile.mtime,afile.parent)
        data.append(t)
    dao = FileDAO('test')
    dao.addfiles(data)
    
def test():
    fl = FTPTraversal('127.0.0.1','z','123')
    l = fl.list()
    for i in l:
        print i
    print l
    fl.logout()
    
def testb():
    now = int(time.time())
    print now
    timeArray = time.localtime(now)
    #otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print timeArray
    print time.localtime( now - 60 )
    print time.localtime( now - 60 * 60 * 24 * 365 * 20)
    
if __name__ == '__main__':
    #travel()
    testb()