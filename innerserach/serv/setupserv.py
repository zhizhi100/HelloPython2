# -*- coding: UTF8 -*-
'''
Created on 2016年2月23日

@author: ZhongPing
'''
from distutils.core import setup  
import py2exe  
import sys  
includes = ["encodings", "encodings.*"]    
sys.argv.append("py2exe")  
options = {"py2exe":   
            {   "compressed": 1
            }   
          }     

setup(service=["serachservice"],
      options = options,  
      zipfile=None,   
      windows = [{"script":'serachservice.py'}])

setup(service=["scheduleservice"],
      options = options,  
      zipfile=None,   
      windows = [{"script":'scheduleservice.py'}])