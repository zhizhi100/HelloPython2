# -*- coding: UTF8 -*-
'''
Created on 2015年11月23日

@author: ZhongPing
'''
import win32serviceutil
import win32service
import win32event
import os
import sys
import time

sys.stopservice = "false"

def main():
    '''
    Modulo principal para windows
    '''
    sys.path.insert(0,os.getcwd())
    import st
    a = st.service_test()

class ServiceLauncher(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ServiceTest'
    _scv_display_name_ ='Servicio de pruebas'
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        sys.stopservice = "true"
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        main()