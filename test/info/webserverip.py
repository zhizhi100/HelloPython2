# -*- coding: UTF8 -*-
'''
Created on 2015年12月9日

@author: ZhongPing
'''
import sys,socket,SocketServer
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        (ip, port) =  self.client_address
        self.wfile.write('hello!')
        self.wfile.write('your ip is:')
        self.wfile.write(ip)

#HandlerClass = SimpleHTTPRequestHandler
HandlerClass = ProxyHandler
ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000

server_address = ('127.0.0.1', port)
local_hostname = socket.gethostname ()
server_address = (socket.gethostbyname (local_hostname), port)
server_address = ('', port)
HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()
