# encoding: utf-8
'''
Created on 2015年12月23日

@author: ZhongPing
'''
import socket

gtdir = ''

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton,cls).__new__(cls, *args, **kwargs)
        return cls._inst
    
class Gtenv(Singleton):
    def __init__(self,envpath):
        self.verison = '1.2.1'
        if not hasattr(self, 'path'):
            self.path = envpath
    def getpath(self):
        return self.path
    
    def getip(self):
        localip = socket.gethostbyname(socket.gethostname())
        return localip
    
    def getlic(self):
        return self.licdate,self.licdays
    
if __name__ == '__main__':
    myenv = Gtenv("")
    print myenv.getip()
'''    
a = Gtenv('a')
b = Gtenv('b')
print a.getpath()
print b.getpath()
'''