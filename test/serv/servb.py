# -*- coding: UTF8 -*-
'''
Created on 2015年11月28日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import thread
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8200, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
        
def startweb():
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()       

def log(message):
        #logger = file("e:\log.txt","a")
        #logger.write(message+"\r\n")
        #logger.close()
        pass


class ServiceB(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "ServB"
        _svc_display_name_ = "ServB"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                thread.start_new(startweb, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
                