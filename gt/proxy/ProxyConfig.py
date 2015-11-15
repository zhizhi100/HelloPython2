# encoding: utf-8
'''
Created on 2015年10月27日

@author: ZhongPing
'''

import os
import json

class config():
    cfgfile = ''
    redirectcfg = {}
    modifycfg = {}
    repostcfg = {}
    
    def __init__(self,file):
        self.cfgfile = file
        
    def _check(self,cfg):
        if not (cfg.has_key('Type') and cfg.has_key('Rules')):
            cfg = {}
            return
        rules = cfg['Rules']
        for r in rules:
            if not(r.has_key('Action') and r.has_key('Content') \
                   and r.has_key('MatchMode') and r.has_key('MatchContent') and r.has_key('Type')):
                rules.remove(r)
            if (r['Action']=='' or r['Content']=='' or r['MatchMode']=='' \
                or r['MatchContent']=='' or r['Type']==''):
                rules.remove(r)
        
    def check(self):
        self._check(self.redirectcfg)
        self._check(self.modifycfg)
        self._check(self.repostcfg)
        
    def read(self):
        if os.path.isfile(self.cfgfile):
            f = file(self.cfgfile)
            j = json.load(f,encoding ='utf-8')
            if j.has_key('Redirect'):
                self.redirectcfg = j['Redirect']
            if j.has_key('Modify'):
                self.modifycfg = j['Modify']
            if j.has_key('Repost'):
                self.repostcfg = j['Repost']                
        self.check()
        return (self.redirectcfg,self.modifycfg,self.repostcfg)
    
    def writ(self):
        if os.path.isfile(self.cfgfile):
            j = {}
            j['Redirect'] = self.redirectcfg
            j['Modify'] = self.modifycfg
            j['Repost'] = self.repostcfg
            s = json.dumps(j,sort_keys=True,indent=4)
            f = file(self.cfgfile,'w+')
            f.write(s)
            f.close()
    
if __name__ == '__main__':
    c = config('config.json')
    (r,m) = c.read()
    print r
    print m
    pass