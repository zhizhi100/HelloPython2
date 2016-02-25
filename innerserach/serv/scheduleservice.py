# -*- coding: UTF8 -*-
'''
Created on 2016年2月23日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import thread

class ScheduleService(win32serviceutil.ServiceFramework):
        #这两行必须
        _svc_name_ = "Inner Schedule Server"
        _svc_display_name_ = "Inner后台服务"
        
        def __init__(self, args):
                win32serviceutil.ServiceFramework.__init__(self, args)
                self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
                
        def SvcStop(self):
                self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                win32event.SetEvent(self.hWaitStop)
                
        def SvcDoRun(self):
                import innerserach.schedule.main 
                thread.start_new(innerserach.schedule.main.startschedule, ())
                win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)