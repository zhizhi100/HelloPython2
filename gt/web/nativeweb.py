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
from reposthandler import Repost,Downloader,GetNsrDetail,JSONP,NsrlistJsonp
from jobhandler import Job,ThreadJob,ImoportNsr
from dbhandler import Querynsr,Querytrace,G3info,SaveRemoteQuery
from remotehandler import RemoteQuery
from gt.gtcore.env import Gtenv,gtdir
import ConfigParser
import gt.license.auth as auth
import gt.license.trial as trial
from gt.gtcore.env import Gtenv
from datetime import date

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
        
class Lic(tornado.web.RequestHandler):
    def get(self):
        myenv = Gtenv("")
        self.write("{istrial:")
        if myenv.istrial:
            self.write("1")
        else:
            self.write("0")
        self.write(",version:'"+myenv.verison)
        self.write("',licdate:'")
        self.write(myenv.licdate.strftime('%Y-%m-%d'))
        self.write("'}")
        
def writelicjs():
    s = ""
    myenv = Gtenv("")
    s = '{"istrial":'
    if myenv.istrial:
        s = s + "1"
    else:
        s = s + "0"
    s = s + ",\"version\":\""+myenv.verison + "\","
    s = s + "\"licdate\":\"" + myenv.licdate.strftime('%Y-%m-%d') + "\"}"
    
    path = myenv.getpath()
    fname = path + "/static/license.js"
    fo = open(fname,'w')
    fo.write(s)
    fo.close()
        
def startweb():
    #parse_command_line is very important
    tornado.options.parse_command_line()
    #print tornado.options.options.as_dict()
    path = sys.path[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    #print path
    gtdir = path
    webenv = Gtenv(path)
    path = webenv.getpath()
    logfile = ''
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(path + "/service.ini")
        logfile = path + "/" + cf.get("log","local")
    except Exception as e:
        pass
    if logfile == '':
        logfile = path + "/" +DEFAULT_LOG_FILENAME    
    
    daemon  = False
    max_log_size = 20
    logger = logSetup (logfile, max_log_size, daemon)
    
    licdays,licdate = trial.haskey()
    if licdays == 0 or (licdate - date.today()).days < 0:
        licdays,licdate = auth.haslic()
        if licdays == 0 or (licdate - date.today()).days < 0:
            logger.warning(u'试用授权到期或没有正式授权文件，系统启动失败！')
            return 0
        else:
            webenv.istrial = False
            webenv.licdate = licdate
    else:
        webenv.istrial = True
        webenv.licdate = licdate
        
    writelicjs()        
    
    settings = {
            "static_path": path + "/static",
            }

    app = tornado.web.Application([
        (r"/", Hello),
        (r"/hello", Hello),
        (r"/getlic", Lic),
        (r"/repost", Repost),
        (r"/job", Job),
        (r"/testjob", ThreadJob),
        (r"/querynsr", Querynsr),
        (r"/querytrace", Querytrace),
        (r"/download",Downloader),
        (r"/importnsr",ImoportNsr),
        (r"/rquery",RemoteQuery),
        (r"/sysinfo",G3info),
        (r"/SaveRemoteQuery",SaveRemoteQuery),
        (r"/jsonp",JSONP),
        (r"/nsrlistjsonp",NsrlistJsonp),
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