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

def startschedule():
    scheduler = BlockingScheduler()
    scheduler.add_job(test,'cron', second='*/3', hour='*')    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()     

if __name__ == '__main__':
    startschedule()