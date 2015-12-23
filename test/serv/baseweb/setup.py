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
            {   "compressed": 1
            }
          }

setup(service=["simpleserv"],
      options = options,  
      zipfile=None,   
      windows = [{"script":'simpleserv.py'}])

setup(service=["proxyserv"],
      options = options,  
      zipfile=None,   
      windows = [{"script":'proxyserv.py'}])