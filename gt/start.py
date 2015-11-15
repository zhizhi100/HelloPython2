# encoding: utf-8
'''
Created on 2015年11月15日

@author: ZhongPing
'''
import sys
import getopt
from gt.web import nativeweb
from gt.proxy import proxy

def usage (msg=None):
    if msg: print msg
    print sys.argv[0], "[-s 服务]"
    print
    print "   -s       - web服务或proxy服务:-s web|-s proxy"
    print

if __name__ == '__main__':
    try: opts, args = getopt.getopt (sys.argv[1:], "l:dhp:", [])
    except getopt.GetoptError, e:
        usage (str (e))
        return 1
        
    for opt, value in opts:
        if opt == "-s": serv = value
        
    if serv=='web':
        nativeweb.startweb()
    elif serv == 'proxy':
        sys.exit (proxy.main ())
    else:
        usage()
        return 0