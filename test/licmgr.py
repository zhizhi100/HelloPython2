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
import rsa,base64

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
    with open('public.key') as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
    randomstr = string.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8)).replace(' ','')
    content = base64.encodestring(rsa.encrypt(randomstr,pubkey))
    dstr = base64.encodestring(rsa.encrypt(d,pubkey))
    content = content + dstr
    randomstr = string.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8)).replace(' ','')
    content = content + base64.encodestring(rsa.encrypt(randomstr,pubkey))
    content = content + base64.encodestring(rsa.encrypt(ip,pubkey))
    randomstr = string.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8)).replace(' ','')
    content = content + base64.encodestring(rsa.encrypt(randomstr,pubkey))
    return content

def decrpt(content):
    with open('private.key') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
    d = content[693:1385]
    d = rsa.decrypt(base64.decodestring(d), privkey)
    ip = content[2079:2771]
    ip = rsa.decrypt(base64.decodestring(ip), privkey)
    return(d,ip)

def test():
    str = '0123456789'
    print str[0:3] #截取第一位到第三位的字符
    if checkip('127.0.0.1'): print iptoint('127.0.0.1')
    t = 'localhost'
    if checkip(t): print iptoint(t)
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")
    #print today
    t = encrpt('20161230', '149.16.19.20')
    decrpt(t)

if __name__ == '__main__':
    test()
    pass