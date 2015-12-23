'''
Created on 2015年12月22日

@author: ZhongPing
'''
# -*- coding: UTF8 -*-
'''
Created on 2015年12月1日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import thread

class SimpleServ(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "Golden Tool simple Server"
        _svc_display_name_ = "金三助手简单服务"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                import simple
                thread.start_new(simple.main, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)