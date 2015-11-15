# encoding: utf-8
'''
Created on 2015年11月12日

@author: ZhongPing
'''

import tornado.web
import threading
from time import ctime,sleep

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
        self.write('a thread will sleep about 10s')
        t = threading.Thread(target=self._job)
        t.setDaemon(True)
        t.start()
        