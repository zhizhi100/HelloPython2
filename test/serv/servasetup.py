# -*- coding: UTF8 -*-
'''
Created on 2015年11月28日

@author: ZhongPing
'''
from distutils.core import setup
import py2exe
import sys  
includes = ["encodings", "encodings.*"]    
sys.argv.append("py2exe")  
options = {"py2exe":   { "bundle_files": 1 }  }

setup(options = options,  
      zipfile=None,  
      service=["serva"])