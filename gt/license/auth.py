# encoding: utf-8
'''
Created on 2015年12月3日

@author: ZhongPing
'''

from datetime import *

def haslic():
    has = 0
    a = date(2015,1,1)
    b = date.today() + timedelta(30)
    has = (b - a).days
    return has,b
    
    
    

if __name__ == '__main__':
    h,t = haslic()
    print h,t 
    pass