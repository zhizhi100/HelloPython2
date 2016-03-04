# -*- coding: UTF8 -*-
'''
Created on 2016年3月1日

@author: ZhongPing
'''
import ConfigParser
import travel
import time

class InnerJob(object):
    def __init__(self,title):
        self.title = title
        self.root = ''
        self.source = ''
        self.host = ''
        self.username = ''
        self.password = ''
        self.enabled = ''

class InnerJobs(object):
    jobs = []
    
    def __init__(self):
        path = 'InnerSearch.ini'
        path = 'E:/workspace/HelloPython2/innerserach/search.config'
        self._read(path) 
        
    def _read(self,config):
        cf = ConfigParser.ConfigParser()
        cf.read(config)
        keys = cf.get('jobs','keys')
        keys = keys.split(',')
        for key in keys:
            job = InnerJob(key)
            sec = 'job_'+key
            source = cf.get(sec,'source')
            if (source == 'file'):
                job.source = source
                job.root = cf.get(sec,'root')
                job.enabled = cf.get(sec,'enabled')
            if (source == 'ftp'):
                job.source = source
                job.root = cf.get(sec,'root')
                job.host = cf.get(sec,'host')
                job.username = cf.get(sec,'username')
                job.password = cf.get(sec,'password')
                job.enabled = cf.get(sec,'enabled')
            self.jobs.append(job)
                
    def printjobs(self):
        for i in self.jobs:
            if i.source == 'file':
                print i.title+':'+i.source+','+i.root
            if i.source == 'ftp':
                print i.title+':'+i.source+',ftp://'+i.username+'@'+i.password+'/'+i.root        
    
    def execjobs(self):
        for i in self.jobs:
            if i.enabled == 'true':
                self.execjob(i)
        
    def execjob(self,job):
        pass
    
    def addjob(self,job):
        self.jobs.append(job)
        
class TrvalJobs(InnerJobs):  
    def execjob(self,job):
        fdao = travel.FileDAO(job.title)        
        if job.source == 'file':
            traveler = travel.FileTravesal()
        if job.source == 'ftp':
            traveler = travel.FTPTraversal(job.host,job.username,job.password)
        if fdao.istravled():
            files = traveler.listfiles(job.root)
            now = int(time.time())
            fromtimestamp = now - 20 * 365 * 24 * 60 * 60
            dirs = fdao.gethotdir(fromtimestamp)
            for dir in dirs:
                t = traveler.listfiles(dir[1])
                files = files + t
        else:
            files = traveler.travel(job.root)
        fdao.addfiles(files)
    
class IndexJobs(InnerJobs):
    def execjob(self,job):
        pass
    
class ContentJobs(InnerJobs):
    def execjob(self,job):
        pass

def test():
    jobs = TrvalJobs()
    #jobs.printjobs()
    jobs.execjobs()
    
if __name__ == '__main__':
    test()    