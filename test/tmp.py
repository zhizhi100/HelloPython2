# encoding: utf-8
'''
Created on 2015年11月13日

@author: ZhongPing
'''
import datetime

if __name__ == '__main__':
    d1 = datetime.datetime.strptime('2012-03-05 23:41:20', '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime('2015-11-13 00:00:00', '%Y-%m-%d %H:%M:%S')
    delta = datetime.datetime.now() - d2
    print delta.days