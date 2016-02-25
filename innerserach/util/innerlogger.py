# encoding: utf-8
'''
Created on 2016年2月23日

@author: ZhongPing
'''
import logging
import logging.config

CONF_LOG = "testlogger.config"  

def logger(qualname):
    logging.config.fileConfig("E:/workspace/HelloPython2/innerserach/logging.conifg") 
    logger = logging.getLogger(qualname)
    return logger

def test():
    logging.config.fileConfig(CONF_LOG);    # 采用配置文件
    logger = logging.getLogger("test")
    logger.debug("Hello logger")
    
    logger = logging.getLogger()
    logger.info("Hello root")

if __name__ == '__main__':
    test()