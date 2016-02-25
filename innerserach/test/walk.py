# -*- coding: UTF8 -*-
'''
Created on 2016年2月24日

@author: ZhongPing
'''

import os

def main():
    path = 'D:/tmp'
    for i in os.listdir(path):
        f = os.path.join(path,i)
        finfo = os.stat(f)
        print finfo.st_mtime
    '''
    for root, dirs, files in os.walk( path ):
        for dir in dirs:
            print os.path.join(root,dir)
            print root,dir
        for fn in files:
            print os.path.join(root,fn)
            print root, fn
    '''
    #for i in os.walk(path):
        #print i[1]
    

if __name__ == '__main__':
    main()