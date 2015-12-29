# encoding: utf-8
'''
Created on 2015年12月3日

@author: ZhongPing
'''
from gt.gtcore.env import Gtenv
import rsa,base64
from datetime import *
import os

def decrpt(content):
    myenv = Gtenv("") 
    path = myenv.getpath() 
    with open(path+'/proxy.dll') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
    d = content[693:1385]
    d = rsa.decrypt(base64.decodestring(d), privkey)
    ip = content[2079:2771]
    ip = rsa.decrypt(base64.decodestring(ip), privkey)
    return(d,ip)

def haslic():
    myenv = Gtenv("") 
    path = myenv.getpath()
    localip = myenv.getip()
    licfile = path + "/" + localip + ".lic"
    if not os.path.isfile(licfile):
        return 0,date.today() + timedelta(-1)
    fobject = open(licfile)
    content = ""
    try:
        content = fobject.read()
    finally:
        fobject.close()
    (d,ip) = decrpt(content)
    if ip != localip:
        return 0,date.today() + timedelta(-1)
    b = datetime.strptime(d,"%Y%m%d")
    b = b.date()
    a = date(2015,1,1)
    has = (b - a).days
    return has,b  

if __name__ == '__main__':
    h,t = haslic()
    print h,t 
    pass