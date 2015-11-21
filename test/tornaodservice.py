# encoding: utf-8
'''
Created on 2015年11月21日

@author: ZhongPing
'''
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.httpclient import HTTPClient
import random

r = random.randint(1, 20000)

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")
        
class Stop(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument("key", -1)
        if self.request.remote_ip == '127.0.0.1':
            self.write('Your web server will self destruct soon.')            
            ioloop = tornado.ioloop.IOLoop.instance()
            ioloop.stop()
        
class Server(object):
    logger = None
    ioloop = None
    port = 8001
    def __init__(self): 
        logger = logging.getLogger ("Golden NativeWeb")
        logger.setLevel (0)
        handler = logging.handlers.RotatingFileHandler ('tornadoservice',
                                                        maxBytes=(5*(1<<20)),
                                                        backupCount=5)
        fmt = logging.Formatter ("[%(asctime)-12s.%(msecs)03d] "
                                 "%(levelname)-8s"
                                 " %(message)s",
                                 "%Y-%m-%d %H:%M:%S")
        handler.setFormatter (fmt)
        logger.addHandler (handler)    
        accesslog = logging.getLogger("tornado.access")
        accesslog.addHandler(handler)
        self.logger = logger
            
    def start(self):
        tornado.options.parse_command_line()        
        settings = {
                "static_path": "static",
                }
        app = tornado.web.Application([
            (r"/", Hello),
            (r"/hello", Hello),
            (r"/stop",Stop)
            ],**settings)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(self.port)
        self.ioloop = http_server
        self.logger.log(logging.INFO,"Servering HTTP on localhost port:%s",8001)
        self.instance = tornado.ioloop.IOLoop().instance()
        self.instance.start()
        
    def stopsrv(self):
        self.logger.info("Asked Tornado to exit")
        #AsyncHTTPClient().fetch("http://127.0.0.1:"+str(self.port)+"/stop?key="+str(r),None)
        HTTPClient().fetch("http://127.0.0.1:"+str(self.port)+"/stop?key="+str(r))
        
def stopinstance():
    HTTPClient().fetch("http://127.0.0.1:8001/stop")        
        
if __name__ == '__main__':
    import sys
    #for i in range(1, len(sys.argv)):
        #print "参数", i, sys.argv[i]
    s = Server()        
    if len(sys.argv)>1:
        if sys.argv[1]=='start':
            s.start()
        else:
            s.stopsrv()
    else:
        s.stopsrv()
    #s = Server()
    #s.stop()