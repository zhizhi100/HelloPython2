# -*- coding: UTF8 -*-
'''
Created on 2015年12月1日

@author: ZhongPing
'''
from distutils.core import setup  
import py2exe  
import sys  
includes = ["encodings", "encodings.*"]    
sys.argv.append("py2exe")  
options = {"py2exe":   
            {   "compressed": 1,
                "bundle_files": 1 
            }
          }     
setup(service=["proxyservice"],
      options = options,  
      zipfile=None,   
      windows = [{"script":'proxyservice.py'}])