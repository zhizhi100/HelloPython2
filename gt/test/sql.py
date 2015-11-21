# encoding: utf-8
'''
Created on 2015��11��19��

@author: Administrator
'''

import sqlite3

def connect():
    return sqlite3.connect('../gtnsr.db')

def printdata(res):
    l = len(res)
    k = 0
    while k < l:
        i = res[k]
        k = k+1
        print i[0],i[1]
    
def querynsr():
    conn = connect()
    sql = 'select nsrsbh,nsrmc from gt_nsr'
    cu = conn.execute(sql)
    res = cu.fetchall()
    printdata(res)
    
def querylog():
    conn = connect()
    sql = 'select nsrsbh,nsrmc from gt_nsr_access'
    cu = conn.execute(sql)
    res = cu.fetchall()
    printdata(res)    

if __name__ == '__main__':
    #querynsr()
    querylog()
    pass