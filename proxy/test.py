# encoding: utf-8
'''
Created on 2015年10月28日

@author: ZhongPing
'''

import ProxyConfig
import RuleMatch

def init():
    cfgcls = ProxyConfig.config('test.json')
    cfg = cfgcls.read()
    return cfg

def testredirect(rules,path):
    r1 = rules['Redirect']
    r2 = rules['Modify']
    match = RuleMatch.RuleMatch(r1,r2)
    (ismatch,newpath)=match.redirect(path,'*')
    print ismatch
    print newpath

def testmodify():
    pass

if __name__ == '__main__':
    rules = {}
    (rules['Redirect'],rules['Modify']) = init()
    testredirect(rules, 'http://www.hao123.com/test.js')
    testredirect(rules, 'http://www.HasKeyword.com/test.js')
    testredirect(rules, 'http://www.RegexChange.com/test.js')
    testredirect(rules, 'http://www.Equal.com/test.js')
    testredirect(rules, 'http://www.EndWith.com/EndWith.js')
    pass