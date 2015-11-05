# encoding: utf-8
'''
Created on 2015年11月5日

@author: ZhongPing
'''
__doc__ = """Golden Proxy.
  
This is the main entrance of the Golden Proxy.
  
2015/11/05 - Created
"""
import datetime
import time
import random
import string
import socket,struct
import rsa

def iptoint(ip):
    return str(socket.ntohl(struct.unpack('I',socket.inet_aton(ip))[0]))

def intoip(int_ip):
    return socket.inet_ntoa(struct.pack('I',socket.htonl(int_ip)))

def checkip(ip):
    isip = True
    try:
        t = struct.unpack('I',socket.inet_aton(ip))
        if (t <= 2130706433): isip=False
    except:
        isip = False
    return isip

def checkds(ds):
    isdate = True
    try:
        t = time.strptime(ds, "%Y%m%d")
    except:
        isdate = False
    return isdate

def encrpt(d,ip):
    if not(checkds(d)):return ''
    if not(checkip(ip)):return ''
    content = ''
    for i in range(1,101):
        content = content + string.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()`~,./;[]<>?:"{}', 10)).replace(' ','')        
    pass

def decrept():
    pass

def test():
    
    if checkip('127.0.0.1'): print iptoint('127.0.0.1')
    t = 'localhost'
    if checkip(t): print iptoint(t)
    '''
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    print today
    print datetime.date.today()
    print random.sample('zyxwvutsrqponmlkjihgfedcba',5)
    print string.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()`~,./;[]<>?:"{}', 10)).replace(' ','')
    content = ''
    for i in range(1,100):
        content = content + string.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()`~,./;[]<>?:"{}', 10)).replace(' ','')        
    print content
    for i in range(1,5):
        print i
    if checkds("20151105"): print time.strptime("20151105", "%Y%m%d")          
    '''     

if __name__ == '__main__':
    test()
    pass