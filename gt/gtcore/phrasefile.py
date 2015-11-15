# encoding: utf-8
'''
Created on 2015年11月13日

@author: ZhongPing
'''
from nsr import Nsr

import logging
import os
import re
from _ssl import txt2obj

class Worker(object):
    
    def savensr(self,nsr):
        pass

class Htmlworker(Worker):
    file = ''
    bfsize = 1024
    cols = []
    
    def __init__(self,path='download.tmp'):
        str = 'nsrsbh|nsrmc|nsrztmc|kzztdjlxmc|djzclxmc|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|hymc|NotConfirmed|scjydz|fddbrxm|fddbrsfzjlxmc|fddbrsfzjhm|djrq|NotConfirmed|zgswskfjmc|ssglymc|jdxzmc|jyfw|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|zcdlxdh|scjydlxdh|fddbrgddh|fddbryddh|bsrxm|bsrgddh|bsryddh|cwfzrxm|cwfzrgddh|cwfzryddh|fjmqybz|kqccsztdjbz|NotConfirmed|NotConfirmed|lrrq|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|shxydm|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed|NotConfirmed'
        self.cols = str.split('|')
        self.file = path
        
    def cut(self,str):
        info = re.compile('<style>.+</style>')#<style></style>
        str = info.sub('',str)   
        info = re.compile('<head>.+</head>')#<head></head>
        str = info.sub('',str)
        info = re.compile('[if.+?\[endif]')#[if supportMisalignedColumns]><tr ><td></td><td></td></tr><![endif]
        str = info.sub('',str)
        return str
    
    def dealnsr(self,data):
        nsr = Nsr()
        info = nsr.getinfo()
        for i in range(len(data)):
            info[self.cols[i]]=data[i]
        succ,msg = nsr.save(info)
        if not succ:logging.warn(msg)
    
    def phraserow(self,str):
        str = str.replace('<tr>', '')
        str = str.replace('</tr>', '')
        str = re.sub('td\s*>','t>',str)
        #print str
        row = re.findall('<t.+?</t>', str)
        if len(row)== 69:
            if row[0].find('纳税人') > -1:
                for k in row:
                    print k
                return #标题栏
            for k in range(69):
                i = row[k]
                i=i.replace('<t>','')
                i=i.replace('</t>','')
                row[k] = i
            self.dealnsr(row)
        
    def getrows(self,str):
        rows = re.findall('<tr.+?</tr>', str)#<tr></tr># <td></td>-><t></t> i don't know why
        for row in rows:
            self.phraserow(row)
        info = re.compile('<tr.+?</tr>')#<tr></tr># <td></td>-><t></t> i don't know why 
        str = info.sub('',str)
        return str
        
    def work(self):
        f = open(self.file, 'rb')
        str = ''
        try:
            while True:
                txt = f.read(1024)
                if not txt:
                    break
                txt = self.cut(txt)
                str = str + txt
                str = cut(str)
                str = self.getrows(str)
                #print len(str)
        finally:
            print str
            f.close()

def testhtmlwork():
    hw =  Htmlworker('nsrlist.txt')
    hw.work()
    
    
def cut(str):
    info = re.compile('<style>.+</style>')#<style></style>
    str = info.sub('',str)   
    info = re.compile('<head>.+</head>')#<head></head>
    str = info.sub('',str)
    info = re.compile('[if.+?\[endif]')#[if supportMisalignedColumns]><tr ><td></td><td></td></tr><![endif]
    str = info.sub('',str)
    '''
    info = re.compile('\<link.+?\/\>')#<link rel="File-List" href="tt.files/filelist.xml" />
    str = info.sub('',str)    
    info = re.compile('\<\!--.+?--\/\>')#<!--table -->
    str = info.sub('',str) 
    info = re.compile('\<meta.+?\>')#<meta name=Generator content='Microsoft Excel 11'>
    str = info.sub('',str)    
    info = re.compile('\{.+?\}')#{....}
    str = info.sub('',str)
    info = re.compile('\<x:.+?\>.*?\<\/x:.+?\>')#<x:ActiveRow>4</x:ActiveRow>
    str = info.sub('',str)
    '''
    return str

def getrow(str):   
    info = re.compile('<tr.+</tr>')#<tr></tr># <td></td>-><t></t> i don't know why 
    match = info.search(str)
    if match:
        print match.group() 
    str = info.sub('',str)
    return str
    
def test():
    print re.split('\W+', 'Words, words, words.') 
    str = '<tr><td>纳税人识别号</td><td>纳税人名称</td><td>纳税人状态</td><td>课征主体登记类型</td><td>登记注册类型</td></tr>'
    items =  re.findall('<td.+?</td>', str)
    for i in items:
        print i    
    items =  re.findall('\<td.+?\<\/td\>', str)
    for i in items:
        print i
    print items
    info = re.compile('\<td.+?\<\/td\>') 
    print cut(str)
    str = cut(str)
    print getrow(str)
    #print cut('<x:CodeName>Sheet3</x:CodeName>')
    return
    f = open('nsrlist.txt', 'rb')
    str = ''
    try:
        while True:
            txt = f.read(1024)
            if not txt:
                break
            txt = cut(txt)
            str = str + txt
            str = cut(str)
            str = getrow(str)
            #print len(str)
    finally:
        print str
        f.close()
        
if __name__ == '__main__':
    #test()       
    testhtmlwork() 