# encoding: utf-8
'''
Created on 2015年11月12日

@author: ZhongPing
'''
import json

class Nsr(object):
    '''
    classdocs
    '''
    info = {}

    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    def getxxfromquery(self,js):
        try:
            d = json.loads(js)
            self.info = d['data'][1]['trs'][0]['tds']
        finally:
            return self.info
        
if __name__ == '__main__':
    f = open('nsrxx.txt')
    try:
        js = f.read()
    finally:
        f.close()
    nsr = Nsr()
    nsr.getxxfromquery(js)        