# -*- coding: UTF8 -*-
'''
Created on 2015年12月22日

@author: ZhongPing
'''
import sys,os
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.wfile.write("I'm OK!\r\n")
        self.wfile.write("os.getcwd():"+os.getcwd()+"\r\n")
        self.wfile.write("sys.argv[0]:"+sys.argv[0]+"\r\n")
        import getpath
        self.wfile.write("I'm from an other py file!\r\n")
        self.wfile.write("os.getcwd():"+getpath.getcwd()+"\r\n")
        self.wfile.write("sys.argv[0]:"+getpath.getarg0()+"\r\n")        

def main():
    serveaddr=('',8000)
    httpd=HTTPServer(serveaddr,MyHandler)
    print "Base serve is start add is %s port is %d"%(serveaddr[0],serveaddr[1])
    httpd.serve_forever()    

if __name__ == '__main__':
    main()