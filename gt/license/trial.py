# encoding: utf-8
'''
Created on 2015年12月3日

@author: ZhongPing
'''

import sys,os
import wmi
import hashlib 
from datetime import date
import datetime   

m2 = hashlib.md5() 

def mymd5(t):
    m2.update(t)
    p = m2.hexdigest()
    #p = p.upper()
    return p

def getid():
    c = wmi.WMI()
    id = ''
    for cpu in c.Win32_Processor():
        id = cpu.ProcessorId.strip()
        break  
    m2.update(id)   
    key = m2.hexdigest()
    key = key.upper()
    return key

def haskey():
    has = 0
    from gt.gtcore.env import Gtenv
    myenv = Gtenv("")
    path = myenv.getpath()
    f = path + '/key.triallic'
    if os.path.exists(f):
        file_object = open(f)
        key = ''
        try:
            key = file_object.read( )
        finally:
            file_object.close( )
        if len(key)>8:
            key1 = key[0:4]
            key2 = key[4:7]
            key3 = key[7:12]
            machid = getid()
            days = int(key2,16)
            if days < 9999:
                days = days % 1000
                a = date(2015,1,1)
                a = a + datetime.timedelta(days)
                s = a.strftime('%Y%m%d')
                s = machid + s
                t = mymd5(s)
                s = t[0:1] + t[8:9] + t[16:17] + t[24:25]
                if key1 == s:
                    s = machid + key1 + key2 + a.strftime('%Y%m%d')
                    t = mymd5(s)
                    s = t[0:1] + t[8:9] + t[16:17] + t[24:25] + t[31:32]
                    if key3 == s:               
                        has = days 
    if has > 730:
        has = 0
    return has,date(2015,1,1) + datetime.timedelta(has)           
          
def test():
    key = '01234567890ab'
    print key[0:1]
    key1 = key[0:4]
    key2 = key[4:7]
    key3 = key[7:12]
    print key1
    print key2
    print key3
    a = date(2015,1,1)
    print a.strftime('%Y%m%d')
            
if __name__ == '__main__':
    test()
    print getid()