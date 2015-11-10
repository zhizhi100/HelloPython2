# -*- coding: utf-8 -*-
'''
Created on 2015年11月9日

@author: ZhongPing
'''
import sys
import getopt
import datetime
import licmgr as lic

def generatelic(d,ip,f):
    c = lic.encrpt(d,ip)
    if (len(c)>0):
        h = open(f,"w+")
        try:
            h.write(c)
        except:
            print 'License文件写入失败，请检查文件名是否正确。'
        finally:
            h.close()
    else:
        print '生成License文件失败，请检查输入的数据是否准确。'
        
def usage (msg=None):
    if msg: print msg
    print sys.argv[0], "[-d 日期] [-p IP地址] [-f 文件名]"
    print
    print "   -d       - 有效日期，格式如20151201，默认为30天以后"
    print "   -P       - IP地址，默认为192.168.0.1，不允许为127.0.0.1"
    print "   -f       - 日志文件名，默认为 IP_D.lic"
    print
    
if __name__ == '__main__':
    d = (datetime.datetime.now()+datetime.timedelta(30)).strftime("%Y%m%d")
    ip = '192.168.0.1'
    f = None
    try: opts, args = getopt.getopt (sys.argv[1:], "l:dhp:", [])
    except getopt.GetoptError, e:
        usage (str (e))
        exit(0)
    for opt, value in opts:
        if opt == "-d": d = value
        if opt == "-p": ip = value
        if opt == "-f": f = value
        if opt == "-h":
            usage ()
            exit(0)
    if f == None:
        f = ip+"_"+d+".lic"
    generatelic(d,ip,f)
    pass