# -*- coding: utf-8 -*-
'''
Created on 2015年11月10日

@author: ZhongPing
'''

import datetime

if __name__ == '__main__':
    t = 'https://www.tmall.com/wow/act/14700/nvzhuang?spm=875.7789098.2015004.d1.S98jIs&acm=lb-zebra-17931-303882.1003.2.505167&aldid=yNQimEpU&scm=1003.2.lb-zebra-17931-303882.ITEM_1444236867984_505167&pos=1'
    print datetime.datetime.now()
    for i in range(1,10001):
        k = t.find('spm')
    print datetime.datetime.now()
    