# encoding: utf-8
'''
Created on 2015年11月12日

@author: ZhongPing
'''
import os
import tornado.web
import threading
import logging
from time import ctime,sleep
from gt.gtcore.phrasefile import Htmlworker

def dosth():
    sleep(5)
    print 'I\'v sleeped 5 s!'
    sleep(5)

class Job(tornado.web.RequestHandler):
    def _work(self):
        self.write('this job is just for test')
        
    def get(self):
        self._work()
        
    def post(self):
        self._work()
        
class ThreadJob(Job):
    def _job(self):
        sleep(5)
        print self.request.headers
        print 'I\'v sleeped 5 s!'
        sleep(5)  
        print 'I\'v sleeped other 5 s!'      
    
    def _work(self):
        self.set_status(200)
        self.finish()
        t = threading.Thread(target=self._job)
        t.setDaemon(True)
        t.start()
        

class ImoportNsr(ThreadJob):
    def _job(self):
        logging.info('begin to import nsr data')
        f = self.get_argument('file')
        if f is not None:
            hw =  Htmlworker(f)
            hw.work()
            os.remove(f)
        logging.info('finished of importing nsr data')