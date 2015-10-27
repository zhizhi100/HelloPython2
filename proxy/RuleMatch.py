# encoding: utf-8
'''
Created on 2015年10月27日

@author: ZhongPing
'''
import re


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
                if i == '*':allredirect = True       
        
        if rdtrules.has_key('Rules'):#有转发规则
            self.redirectrules = rdtrules['Rules']    

        if mdfrules.has_key('Type'):#不为空
            if mdfrules['Type'] == '*':
                self.modifytype = mdfrules['Type']
                for i in self.modifytype:
                    if i== '*':modifyall = True
        
        if mdfrules.has_key('Rules'):#有改写规则
            self.mdfrules = rdtrules['Rules']    
    
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
            return path.find(content) == path.length() - content.length() - 1
        return False
    
    def redirectpath(self,rule,path):
        action = rule['Action']
        content = rule['Contetnt']
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
        return None
    
    def redirect(self,path,accepttype):
        need = False
        if not(self.allredirect):
            for i in self.redirecttype:
                if (i == accepttype):
                    need = True
                    break
        if not(self.allredirect) and not(need):#不需要跳转的类型
            return (False,'')
        for r in self.redirectrules:
            if self.matchpath(r, path):
                break
                