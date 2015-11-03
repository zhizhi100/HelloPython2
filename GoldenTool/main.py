# encoding: utf-8
'''
Created on 2015年11月3日

@author: ZhongPing
'''

import proxy
import nativeweb
import threading
from multiprocessing import Process

def startweb():
    nativeweb.startweb()
    
def startproxy():
    proxy.main()

def main():
    threads = []
    t1 = threading.Thread(target=startweb)
    t2 = threading.Thread(target=startproxy)
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
        
def mainprocess():
    p1 = Process(target=startweb)
    p1.start()
    p2 = Process(target=startproxy)
    p2.start()

if __name__ == '__main__':
    mainprocess()
    pass