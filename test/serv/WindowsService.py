# encoding: utf-8
'''
Created on 2015-11-23

@author: ZhongPing
'''

import win32serviceutil
import win32service
import win32event
import thread

def log(message):
        #logger = file("e:\log.txt","a")
        #logger.write(message+"\r\n")
        #logger.close()
        pass


class WindowsService(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "TestServer"
        _svc_display_name_ = "TestServer"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                import WebServer
                thread.start_new(WebServer.main, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)