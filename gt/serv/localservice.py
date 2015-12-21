# -*- coding: UTF8 -*-
'''
Created on 2015年12月1日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import thread

def log(message):
        logger = file("e:\log.txt","a")
        logger.write(message+"\r\n")
        logger.close()

class LocalService(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "Golden Tool Local Server"
        _svc_display_name_ = "金三助手本地服务"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                import gt.web.nativeweb 
                thread.start_new(gt.web.nativeweb.startweb, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)