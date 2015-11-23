# -*- coding: UTF8 -*-
'''
Created on 2015年11月23日

@author: ZhongPing
'''
import time
import thread
import os
import sys

class service_test:
    def __init__(self):
        thread.start_new(self.do_something, tuple())
        while True:
            if getattr(sys,'stopservice', False):
                sys.exit()
            time.sleep(0.3)

    def do_something(self):
        '''
        Do something
        '''
        while True:
            fname ='E:\\\\test.txt'
            f = open(fname , 'a')
            f.write(time.time())
            f.close()
            time.sleep(1)


if __name__ == "__main__":
    tst = service_test()