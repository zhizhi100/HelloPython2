# encoding: utf-8
#define INCLUDE_SHELL
'''
Created on 2015年11月3日

@author: ZhongPing
'''
import sys,os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import logging
import time
import signal
from tornado.options import define, options
from reposthandler import Repost,Downloader,GetNsrDetail
from jobhandler import Job,ThreadJob,ImoportNsr
from dbhandler import Querynsr,Querytrace

DEFAULT_LOG_FILENAME = "nativeweb.log"

def logSetup (filename, log_size, daemon):
    logger = logging.getLogger ("Golden NativeWeb")
    logger.setLevel (-1000)

    handler = logging.handlers.RotatingFileHandler (filename,
                                                    maxBytes=(log_size*(1<<20)),
                                                    backupCount=5)
    fmt = logging.Formatter ("[%(asctime)-12s.%(msecs)03d] "
                             "%(levelname)-8s"
                             " %(message)s",
                             "%Y-%m-%d %H:%M:%S")
    handler.setFormatter (fmt)
    
    console = logging.StreamHandler()
    console.setLevel(-1000)
    logger.addHandler(console)
  
    logger.addHandler (handler)
    
    accesslog = logging.getLogger("tornado.access")
    accesslog.addHandler(handler)
    #accesslog.addHandler(console)
    
    generallog = logging.getLogger("tornado.general")
    generallog.addHandler(handler)   
    
    applicationlog = logging.getLogger("tornado.application")
    applicationlog.addHandler(handler)
    
    return logger

def sig_handler(sig, frame):
    global logger
    logger.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)
    
def shutdown():
    global logger
    logger.info('Stopping http server')
    global http_server
    http_server.stop() # 不接收新的 HTTP 请求

    logging.info('Will shutdown in %s seconds ...', 5)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 5

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop() # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            logging.info('Shutdown')
    stop_loop()    

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")     
        
def startweb():
    #parse_command_line is very important
    tornado.options.parse_command_line()
    #print tornado.options.options.as_dict()
    path = sys.path[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    logfile = path + '/' + DEFAULT_LOG_FILENAME
    daemon  = False
    max_log_size = 20
    logger = logSetup (logfile, max_log_size, daemon)
    
    settings = {
            "static_path": "static",
            }

    app = tornado.web.Application([
        (r"/", Hello),
        (r"/hello", Hello),
        (r"/repost", Repost),
        (r"/job", Job),
        (r"/testjob", ThreadJob),
        (r"/querynsr", Querynsr),
        (r"/querytrace", Querytrace),
        (r"/download",Downloader),
        (r"/importnsr",ImoportNsr),
        (r"/nsrinfo",GetNsrDetail)
        ],**settings)
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8001)
    logger.log(logging.INFO,"Servering HTTP on localhost port:%s",8001)
    
    #signal never work in windows system
    #signal.signal(signal.SIGTERM, sig_handler)
    #signal.signal(signal.SIGINT, sig_handler)
    try:
        tornado.ioloop.IOLoop.instance().start()
    #KeyboardInterrupt never work
    #except KeyboardInterrupt:
    #    logger.log(logging.INFO,"KeyboardInterrupt")
    #    shutdown()
    except Exception as e:
        print e
        logger.log(logging.INFO,"exception")

if __name__ == '__main__':
    startweb()