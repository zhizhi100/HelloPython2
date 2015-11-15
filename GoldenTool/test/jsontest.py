# encoding: utf-8
'''
Created on 2015年10月27日

@author: ZhongPing
'''
import json

def testjson():
    config = {}
    config['ModifyType']='html'
    rules = {}
    rules['R1']={'Type':'html','Action':'AppendHTML','MatchMode':'StartWith','Contetnt':'<script>alert("Hello!");</script>'}
    rules['R2']={'Type':'html','Action':'AppendHTML','MatchMode':'Regex','Contetnt':'<script>alert("Hello!");</script>'}
    config['Rules'] = rules
    print json.dumps(config,sort_keys=True,indent=4)

def decode():
    f = file('config.json')
    s=json.load(f)
    print s.keys()
    print s['ModifyType']

if __name__ == '__main__':
    print 'json'
    testjson()
    decode()