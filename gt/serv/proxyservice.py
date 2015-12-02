# -*- coding: UTF8 -*-
'''
Created on 2015年12月1日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import thread

class WebService(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "Golden Tool Local Server"
        _svc_display_name_ = "Golden Tool 本地服务"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                import gt.proxy.proxy
                thread.start_new(gt.proxy.proxy.main, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)