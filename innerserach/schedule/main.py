# -*- coding: UTF8 -*-
'''
Created on 2016年2月23日

@author: ZhongPing
'''
import innerserach.util.innerlogger
from apscheduler.schedulers.blocking import BlockingScheduler

def test():
    logger = innerserach.util.innerlogger.logger("test")
    logger.info("hello,I'm tester")
    
def dotraveljobs():
    pass

def doindexjobs():
    pass

def docontentjobs():
    pass

def startschedule():
    scheduler = BlockingScheduler()
    scheduler.add_job(test,'cron', second='*/3', hour='*')    
    scheduler.add_job(dotraveljobs,'cron', second='*/3', hour='*')
    scheduler.add_job(doindexjobs,'cron', second='*/3', hour='*')
    scheduler.add_job(docontentjobs,'cron', second='*/3', hour='*')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()     

if __name__ == '__main__':
    startschedule()