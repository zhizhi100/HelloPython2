# -*- coding: UTF8 -*-
'''
Created on 2016年2月23日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import thread

class SerachService(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "Inner Serach Server"
        _svc_display_name_ = "Inner搜索服务"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                import innerserach.web.main 
                thread.start_new(innerserach.web.main.startweb, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)