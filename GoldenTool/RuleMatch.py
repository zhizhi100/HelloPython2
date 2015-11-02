# encoding: utf-8
'''
Created on 2015年10月27日

@author: ZhongPing
'''
import re
from urllib2 import Request, urlopen, URLError, HTTPError 
import gzip
from StringIO import StringIO
import copy

class RuleMatch():
    allredirect = False
    redirecttype = []
    redirectrules = None
    modifyall = False
    modifytype = []
    modifyrules = None
    
    def __init__(self,rdtrules,mdfrules):
        if rdtrules.has_key('Type'):#不为空
            redirecttype = rdtrules['Type']
            for i in redirecttype:
                if i == '*' :
                    self.allredirect = True
                    break       
        
        if rdtrules.has_key('Rules'):#有转发规则
            self.redirectrules = rdtrules['Rules']    

        if mdfrules.has_key('Type'):#不为空
            self.modifytype = mdfrules['Type']
            for i in self.modifytype:
                if i== '*':modifyall = True
        
        if mdfrules.has_key('Rules'):#有改写规则
            self.mdfrules = mdfrules['Rules']    
    
    #match mode:StartWith,HasKeyword,Regex,Equal,EndWith
    def matchpath(self,rule,path):
        mode = rule['MatchMode']
        content = rule['MatchContent']
        if mode == 'StartWith':#起始字符串
            if path.find(content) == 0:
                return True
            else:
                return False
        elif mode == 'HasKeyword':#有关键字
            if path.find(content) > -1:
                return True
            else:
                return False
        elif mode == 'Regex':#正则表达式
            if re.search(content, path) == None:
                return False
            else:
                return True
        elif mode == 'Equal':#等于
            return content == path
        elif mode == 'EndWith':#结束字符
            a = path.find(content)
            b = len(path) - len(content) 
            return a == b
        return False
    
    #redirect mode:Change,ChangeHost(not finished),ChangeKeyword,RegexChange
    def redirectpath(self,rule,path):
        action = rule['Action']
        content = rule['Content']
        if action == 'Change':
            return content
        elif action == 'ChangeHost':
            return path
        elif action == 'ChangeKeyword':
            keywords = content.split('|')#|
            if len(keywords)==2:
                return path.replace(keywords[0],keywords[1])
            else:
                return path
        elif action == 'RegexChange':
            keywords = content.split('|')#|
            if len(keywords)==2:
                info = re.compile(keywords[0])
                return info.sub(keywords[1],path)
            else:
                return path
        return path
    
    def redirect(self,path,accepttype):
        need = False
        if not(self.allredirect):
            for i in self.redirecttype:
                if (i == accepttype):
                    need = True
                    break
        if not(self.allredirect) and not(need):#不需要跳转的类型
            return (False,path)
        for r in self.redirectrules:
            if self.matchpath(r, path):
                return (True,self.redirectpath(r, path))
        return (False,path)
    
    def getdoc(self,path,reqheaders):
        l_headers = copy.copy(reqheaders)
        if l_headers.has_key('if-modified-since'): del l_headers['if-modified-since']
        if l_headers.has_key('If-None-Match'): del l_headers['If-None-Match']
        #print l_headers
        idoc = ''
        code = ''
        errmsg = ''
        receive_header = {}
        req = Request(path,headers=l_headers)
        try:
            r = urlopen(req)
            idoc = r.read()
            code = r.getcode()
            receive_header = r.info()   
            del receive_header['Content-Encoding']
            if receive_header.get('Content-Encoding') == 'gzip': # and receive_header.get('Content-type').find('html'):
                buf = StringIO(idoc)
                f = gzip.GzipFile(fileobj=buf)
                idoc = f.read()                     
        except HTTPError, e:
            errmsg = 'HTTPError:'+e.msg
        except URLError, e:
            errmsg = 'URLError:'+e.reason()
        return (code,idoc,receive_header,errmsg)
    
    #modify mode:AppendHTML,ChangeKeyword,RegexChange
    def modifyhtml(self,rule,html):
        #if html encode type is not utf8,may raise error
        action = rule['Action']
        content = rule['Content'].decode('ascii','ignore').encode('utf-8')
        if action == 'AppendHTML':
            html = html + content
            return html
        elif action == 'ChangeKeyword':
            keywords = content.split('|')#|
            if len(keywords)==2:
                html =  html.replace(keywords[0],keywords[1])
                return html
            else:
                return html
        elif action == 'RegexChange':
            keywords = content.split('|')#|
            if len(keywords)==2:
                info = re.compile(keywords[0])
                html =  info.sub(keywords[1],html)
                return html
            else:
                return None
        else:
            return None               
    
    def modify(self,path,accepttype,headers):
        need = False
        for i in self.modifytype:
            if (i == accepttype):
                need = True
                for j in self.mdfrules:
                    if self.matchpath(j, path):
                        (responsecode,html,receive_header,errormsg) = self.getdoc(path, headers)
                        if not(errormsg == ''):
                            return (True,errormsg,None)
                        else:
                            resp = {}
                            resp['code'] = responsecode
                            resp['html'] = self.modifyhtml(j, html)
                            resp['header'] = receive_header
                            return (True,'',resp)
                    else:
                        need = False
                break
        if not(need): return (False,'',None)#do not need modify html
        
if __name__ == '__main__':
    print 'json'
