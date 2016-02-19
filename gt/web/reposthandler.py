# encoding: utf-8
'''
Created on 2015年11月11日

@author: ZhongPing
'''
import os
import json
import logging
import time
import threading
import tornado.web
import tornado.httpclient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tornado.web import HTTPError, asynchronous
import urlparse,urllib

class Reget(tornado.web.RequestHandler):
    @asynchronous
    def get(self):
        headers = dict(self.request.headers)
        url = ''
        if headers.has_key('Gtool_url'):
            url = headers['Gtool_url']
            del headers['Gtool_url']
        else:
            raise HTTPError(500)
        try:
            logging.info('to fecth url:%s',url)
            #self._before_post(self.request)
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
            logging.info('finished in fecthing url:%s',url)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)
                 
    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location", "Content-Disposition"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            if response.body:
                self.write(response.body)
            self.finish()
            self._on_success(response)
            
    def _on_success(self,response):
        pass

class Repost(tornado.web.RequestHandler):
    def get(self):
        self.write("just for test") 
        
    @asynchronous
    def post(self):
        headers = dict(self.request.headers)
        url = ''
        if headers.has_key('Gtool_url'):
            url = headers['Gtool_url']
            del headers['Gtool_url']
        else:
            raise HTTPError(500)
        #print headers
        #print self.request.body 
        try:
            logging.info('to fecth url:%s',url)
            #self._before_post(self.request)
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
            logging.info('finished in fecthing url:%s',url)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)
                
    def _before_post(self,request):
        pass
                       
    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location", "Content-Disposition"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            
            '''
            for k,v in response.headers.items():
                self.set_header(k, v)
            '''
            #print response.body
            if response.body:
                self.write(response.body)
            self.finish()
            self._on_success(response)
            
    def _on_success(self,response):
        pass
    
class Test(Repost):
    def _on_success(self,response):
        if response.body:
            print response.body
            
class Loadnsr(Repost):
    def _on_success(self,response):
        if response.body:
            pass
        
class GetNsrDetail(Repost):
    def _on_success(self, response):
        if response.body:
            from gt.gtcore.nsr import UNsr
            from gt.gtcore.env import Gtenv
            env = Gtenv("")
            uid = env.uid
            #print uid
            if uid:
                nsr = UNsr(uid)
                info = nsr.getxxfromquery(response.body)
                nsr.savetrace(info)
                nsr.save(info)
        
class Downloader(Repost):
    def test(self):
        from time import ctime,sleep
        sleep(6)
    
    def newjob(self,target):
        t = threading.Thread(target=target)
        t.setDaemon(True)
        t.start()
    
    def storensr(self,txt):
        r = int(time.time())
        f = 'tmp'+str(r)+'.data'
        fo = open(f,'w')
        try:
            fo.write(txt)
        finally:
            fo.close()
        AsyncHTTPClient().fetch(
            HTTPRequest(url='http://127.0.0.1:8001/importnsr?file='+f,
                        method="GET",
                        follow_redirects=False),
            None)
    
    def isdownloadnsrlist(self,data):
        isnsr = False
        if data is not None: #is 税务登记信息查询
            data = json.loads(data)
            if data.has_key('data'):
                data = data['data']
                if len(data)==1:
                    data = data[0]
                    if data.has_key('value'):
                        data = data['value']
                        data = json.loads(data)
                        data = data['sqlmc']
                        if data==u'\u7a0e\u52a1\u767b\u8bb0\u4fe1\u606f\u67e5\u8be2': #税务登记信息查询
                            isnsr = True       
        return isnsr
    
    def _on_success(self,response):
        if response.body:
            data = self.get_argument('postData',None)
            if self.isdownloadnsrlist(data):
                self.storensr(response.body)
                #self.newjob(self.storensr(response.body))
                #self.newjob(self.test())
                #logging.info('to new thread deal with database')
                #t = threading.Thread(target=self.storensr(response.body))
                #t.setDaemon(True)
                #t.start()


class JSONP(Repost):    
    funcname = ''
    data = {}
    
    @asynchronous
    def get(self):
        headers = dict(self.request.headers)
        if headers.has_key('Gtool_url'):
            url = headers['Gtool_url']
            del headers['Gtool_url']
        else:
            raise HTTPError(500)
        u = urlparse.urlparse(url)
        p = u[4]
        k = p.split('&')
        for i in k:
            s = i.split("=")
            if len(s)==2:
                self.data[s[0]]=s[1]
            
        if self.data.has_key('callback'):
            self.funcname = self.data['callback']
        #p = url.find('&callback=jQueryGtool')
        #if p > 0:
        #    url = url[0:p]
        #print url
        #print headers
        #print self.request.body 
        try:
            logging.info('to fecth url:%s',url)
            self._before_post(self.request)
            AsyncHTTPClient().fetch(
                HTTPRequest(url=url,
                            method="POST",
                            body=self.request.body,
                            headers=headers,
                            follow_redirects=False),
                self._on_proxy)
            logging.info('finished in fecthing url:%s',url)
        except tornado.httpclient.HTTPError, x:
            if hasattr(x, "response") and x.response:
                self._on_proxy(x.response)
            else:
                logging.error("Tornado signalled HTTPError %s", x)    
    
    def _before_post(self,request):
        if self.data.has_key("gtool_remotelistnsr"):
            arr = []
            #arr.append("sqlxh="+ self.data['sqlxh'])
            arr.append("sqlxh=10010002")
            arr.append('dmtomc=[{"dm":"DJZCLX_DM","dmweb":"DJZCLX_DM","mc":"DJZCLXMC","dmb":"DM_DJ_DJZCLX"},{"dm":"GDGHLX_DM","dmweb":"GDGHLX_DM","mc":"GDGHLXMC","dmb":"DM_DJ_GDGHLX"},{"dm":"KZZTDJLX_DM","dmweb":"KZZTDJLX_DM","mc":"KZZTDJLXMC","dmb":"DM_DJ_KZZTDJLX"},{"dm":"SWDJBZFS_DM","dmweb":"BZFS_DM","mc":"SWDJBZFSMC","dmb":"DM_DJ_SWDJBZFS"},{"dm":"ZFJGLX_DM","dmweb":"ZFJGLX_DM","mc":"ZFJGLXMC","dmb":"DM_DJ_ZFJGLX"},{"dm":"DWLSGX_DM","dmweb":"DWLSGX_DM","mc":"DWLSGXMC","dmb":"DM_GY_DWLSGX"},{"dm":"GSXZGLJG_DM","dmweb":"PZSLJG_DM","mc":"GSXZGLJGMC","dmb":"DM_GY_GSXZGLJG"},{"dm":"GYKGLX_DM","dmweb":"GYKGLX_DM","mc":"GYKGLXMC","dmb":"DM_GY_GYKGLX"},{"dm":"HSFS_DM","dmweb":"HSFS_DM","mc":"HSFSMC","dmb":"DM_GY_HSFS"},{"dm":"HY_DM","dmweb":"HYML@HYDL@HYZL@HY_DM","mc":"HYMC","dmb":"DM_GY_HY"},{"dm":"JDXZ_DM","dmweb":"JDXZ_DM","mc":"JDXZMC","dmb":"DM_GY_JDXZ"},{"dm":"KJZDZZ_DM","dmweb":"KJZDZZ_DM","mc":"KJZDZZMC","dmb":"DM_GY_KJZDZZ"},{"dm":"NSRZT_DM","dmweb":"NSRZT_DM","mc":"NSRZTMC","dmb":"DM_GY_NSRZT"},{"dm":"SFBZ_DM","dmweb":"FJMQYBZ@KQCCSZTDJBZ@YXBZ","mc":"SFBZMC","dmb":"DM_GY_SFBZ"},{"dm":"SFZJLX_DM","dmweb":"FDDBRSFZJLX_DM","mc":"SFZJLXMC","dmb":"DM_GY_SFZJLX"},{"dm":"SWJG_DM","dmweb":"ZGSWJ_DM@ZGSWSKFJ_DM","mc":"SWJGMC","dmb":"DM_GY_SWJG"},{"dm":"SWRY_DM","dmweb":"SSGLY_DM@LRR_DM@XGR_DM","mc":"SWRYMC","dmb":"DM_GY_SWRY"},{"dm":"YGZNSRLX_DM","dmweb":"YGZNSRLX_DM","mc":"YGZNSRLXMC","dmb":"DM_GY_YGZNSRLX"},{"dm":"ZZLX_DM","dmweb":"ZZLX_DM","mc":"ZZLXMC","dmb":"DM_GY_ZZLX"}]')            
            arr.append("{name:SFBAHTDZSBM,type:string,value:'N'},{name:YXBZ,type:string,value:'Y'},{name:NSRMC,type:string,value:'a'},{name:DJRQQ,type:string,value:'1971-12-01'}]");
            arr.append("fzzd=")
            arr.append("znl=null")
            arr.append("totalcount=3")
            arr.append("totalflag=1")
            #arr.append("gwssswjg1="+ self.data["gwssswjg1"])
            #arr.append("gwssswjg1=24301811600")
            arr.append("qxswjgstr=")
            mc = self.data['mc']
            mc = urllib.url2pathname(mc)
            swjg = self.data['swjg']
            arr.append("cxsql=SELECT NSR.NSRSBH, NSR.NSRMC, NSR.NSRZT_DM, NSR.KZZTDJLX_DM, /*税务登记类型,已变更*/ NSR.DJZCLX_DM, NSR.GDGHLX_DM, NSR.DWLSGX_DM, (SELECT HY.SJHY_DM FROM DM_GY_HY HY WHERE SUBSTRB(NSR.HY_DM, 1, 2) = HY.HY_DM(+) AND ROWNUM = 1) HYML, SUBSTRB(NSR.HY_DM, 1, 2) HYDL, SUBSTRB(NSR.HY_DM, 1, 3) HYZL, NSR.HY_DM, NSR.ZCDZ, NSR.SCJYDZ, NSR.FDDBRXM, NSR.FDDBRSFZJLX_DM, NSR.FDDBRSFZJHM, NSR.DJRQ, NSR.ZGSWJ_DM, NSR.ZGSWSKFJ_DM, NSR.SSGLY_DM, NSR.JDXZ_DM, KZ.JYFW, KZ.YGZNSRLX_DM, KZ.KJZDZZ_DM, KZ.BZFS_DM, KZ.HSFS_DM, KZ.GYKGLX_DM, KZ.GYTZBL, KZ.ZRRTZBL, KZ.WZTZBL, KZ.ZCZB, KZ.TZZE, KZ.CYRS, KZ.WJCYRS, KZ.HHRS, KZ.GGRS, KZ.GDGRS, HX_ZTSJ.F_CX_DJ_PZJGXX('PZSLJG_DM', NSR.DJXH) PZSLJG_DM, HX_ZTSJ.F_CX_DJ_PZJGXX('ZZLX_DM', NSR.DJXH) ZZLX_DM, HX_ZTSJ.F_CX_DJ_PZJGXX('ZZHM', NSR.DJXH) ZZHM, HX_ZTSJ.F_CX_DJ_PZJGXX('KYSLRQ', NSR.DJXH) KYSLRQ, HX_ZTSJ.F_CX_DJ_PZJGXX('SCJYQXQ', NSR.DJXH) SCJYQXQ, HX_ZTSJ.F_CX_DJ_PZJGXX('SCJYQXZ', NSR.DJXH) SCJYQXZ, KZ.ZCDLXDH, KZ.SCJYDLXDH, KZ.FDDBRGDDH, KZ.FDDBRYDDH, KZ.BSRXM, KZ.BSRGDDH, KZ.BSRYDDH, KZ.CWFZRXM, KZ.CWFZRGDDH, KZ.CWFZRYDDH, NSR.FJMQYBZ, NSR.KQCCSZTDJBZ, NSR.YXBZ, NSR.LRR_DM, NSR.LRRQ, NSR.XGR_DM, NSR.XGRQ, NSR.NSRBM, NSR.SSDABH, NSR.SHXYDM, '联系信息' LXXX, (SELECT '受理信息' FROM DJ_YSQYWSLXXB SL WHERE NSR.DJXH = SL.DJXH AND ROWNUM = 1) SLXX, KZ.ZFJGLX_DM, (SELECT '总机构信息' FROM DJ_ZJGXX ZJG WHERE NSR.DJXH = ZJG.DJXH AND ROWNUM = 1) ZJGXX, (SELECT '分支机构信息' FROM DJ_FZJGXX FZ WHERE NSR.DJXH = FZ.DJXH AND ROWNUM = 1) FZJGXX, NSR.DJXH FROM DJ_NSRXX NSR, DJ_NSRXX_KZ KZ WHERE NSR.DJXH = KZ.DJXH AND NSR.ZGSWJ_DM IN (SELECT SWJG_DM FROM DM_GY_SWJG V START WITH V.SWJG_DM IN ('"+ swjg +"') CONNECT BY PRIOR V.SWJG_DM = V.SJSWJG_DM) AND (('Y' = 'N') OR ('N' = 'N' AND NSR.KZZTDJLX_DM <> '1600')) AND NSR.YXBZ IN ('Y') AND NSR.NSRMC LIKE '%"+mc+"%' AND NSR.DJRQ >= TO_DATE('1971-12-01', 'YYYY-MM-DD')") 
            arr.append("footvalue={}")
            arr.append("page=1")
            arr.append("start=0")
            arr.append("limit=50")
            bodya = "&".join(arr)
            bodya = urllib.quote(bodya,"='&")
            request.body = bodya
        
        
    def _on_proxy(self, response):
        if response.error and not isinstance(response.error,
                                             tornado.httpclient.HTTPError):
            raise HTTPError(500)
        else:
            self.set_status(response.code)
            
            for header in ("Date", "Cache-Control", "Server", "Content-Type", "Location", "Content-Disposition"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            
            '''
            for k,v in response.headers.items():
                self.set_header(k, v)
            '''
            #print response.body
            if response.body:
                s = response.body.strip()
                s = s.replace("'","\\'")
                s = s.replace("\\r\\n","")
                s = s.replace("\\r","")
                s = s.replace("\\n","")
                t = ''.join(self.funcname) + ''
                self.write(t +"('"+s+"');")
                #self.write(response.body)
                #self.write(t +"('{\"name\":\"ZGSWSKFJ_DM\"}')")
                
            self.finish()
            
class NsrlistJsonp(JSONP):
    def _before_post(self,request):
        arr = []
        arr.append("sqlxh="+self.data['sqlxh'])
        arr.append('dmtomc=[{"dm":"DJZCLX_DM","dmweb":"DJZCLX_DM","mc":"DJZCLXMC","dmb":"DM_DJ_DJZCLX"},{"dm":"GDGHLX_DM","dmweb":"GDGHLX_DM","mc":"GDGHLXMC","dmb":"DM_DJ_GDGHLX"},{"dm":"KZZTDJLX_DM","dmweb":"KZZTDJLX_DM","mc":"KZZTDJLXMC","dmb":"DM_DJ_KZZTDJLX"},{"dm":"SWDJBZFS_DM","dmweb":"BZFS_DM","mc":"SWDJBZFSMC","dmb":"DM_DJ_SWDJBZFS"},{"dm":"ZFJGLX_DM","dmweb":"ZFJGLX_DM","mc":"ZFJGLXMC","dmb":"DM_DJ_ZFJGLX"},{"dm":"DWLSGX_DM","dmweb":"DWLSGX_DM","mc":"DWLSGXMC","dmb":"DM_GY_DWLSGX"},{"dm":"GSXZGLJG_DM","dmweb":"PZSLJG_DM","mc":"GSXZGLJGMC","dmb":"DM_GY_GSXZGLJG"},{"dm":"GYKGLX_DM","dmweb":"GYKGLX_DM","mc":"GYKGLXMC","dmb":"DM_GY_GYKGLX"},{"dm":"HSFS_DM","dmweb":"HSFS_DM","mc":"HSFSMC","dmb":"DM_GY_HSFS"},{"dm":"HY_DM","dmweb":"HYML@HYDL@HYZL@HY_DM","mc":"HYMC","dmb":"DM_GY_HY"},{"dm":"JDXZ_DM","dmweb":"JDXZ_DM","mc":"JDXZMC","dmb":"DM_GY_JDXZ"},{"dm":"KJZDZZ_DM","dmweb":"KJZDZZ_DM","mc":"KJZDZZMC","dmb":"DM_GY_KJZDZZ"},{"dm":"NSRZT_DM","dmweb":"NSRZT_DM","mc":"NSRZTMC","dmb":"DM_GY_NSRZT"},{"dm":"SFBZ_DM","dmweb":"FJMQYBZ@KQCCSZTDJBZ@YXBZ","mc":"SFBZMC","dmb":"DM_GY_SFBZ"},{"dm":"SFZJLX_DM","dmweb":"FDDBRSFZJLX_DM","mc":"SFZJLXMC","dmb":"DM_GY_SFZJLX"},{"dm":"SWJG_DM","dmweb":"ZGSWJ_DM@ZGSWSKFJ_DM","mc":"SWJGMC","dmb":"DM_GY_SWJG"},{"dm":"SWRY_DM","dmweb":"SSGLY_DM@LRR_DM@XGR_DM","mc":"SWRYMC","dmb":"DM_GY_SWRY"},{"dm":"YGZNSRLX_DM","dmweb":"YGZNSRLX_DM","mc":"YGZNSRLXMC","dmb":"DM_GY_YGZNSRLX"},{"dm":"ZZLX_DM","dmweb":"ZZLX_DM","mc":"ZZLXMC","dmb":"DM_GY_ZZLX"}]')
        #arr.append('dmtomc=[{"dm":"SWRY_DM","dmweb":"SSGLY_DM@LRR_DM@XGR_DM","mc":"SWRYMC","dmb":"DM_GY_SWRY"}]')
        arr.append("tj=[{name:SFBAHTDZSBM,type:string,value:'N'},{name:YXBZ,type:string,value:'Y'},{name:NSRMC,type:string,value:'a'},{name:DJRQQ,type:string,value:'1971-12-01'}]");
        arr.append("fzzd=")
        arr.append("znl=null")
        arr.append("totalcount=3")
        arr.append("totalflag=1")
        arr.append("gwssswjg1="+self.data["gwssswjg1"])
        arr.append("qxswjgstr=")
        mc = self.data['mc']
        arr.append("cxsql=SELECT NSR.NSRSBH, NSR.NSRMC, NSR.NSRZT_DM, NSR.KZZTDJLX_DM, /*税务登记类型,已变更*/ NSR.DJZCLX_DM, NSR.GDGHLX_DM, NSR.DWLSGX_DM, (SELECT HY.SJHY_DM FROM DM_GY_HY HY WHERE SUBSTRB(NSR.HY_DM, 1, 2) = HY.HY_DM(+) AND ROWNUM = 1) HYML, SUBSTRB(NSR.HY_DM, 1, 2) HYDL, SUBSTRB(NSR.HY_DM, 1, 3) HYZL, NSR.HY_DM, NSR.ZCDZ, NSR.SCJYDZ, NSR.FDDBRXM, NSR.FDDBRSFZJLX_DM, NSR.FDDBRSFZJHM, NSR.DJRQ, NSR.ZGSWJ_DM, NSR.ZGSWSKFJ_DM, NSR.SSGLY_DM, NSR.JDXZ_DM, KZ.JYFW, KZ.YGZNSRLX_DM, KZ.KJZDZZ_DM, KZ.BZFS_DM, KZ.HSFS_DM, KZ.GYKGLX_DM, KZ.GYTZBL, KZ.ZRRTZBL, KZ.WZTZBL, KZ.ZCZB, KZ.TZZE, KZ.CYRS, KZ.WJCYRS, KZ.HHRS, KZ.GGRS, KZ.GDGRS, HX_ZTSJ.F_CX_DJ_PZJGXX('PZSLJG_DM', NSR.DJXH) PZSLJG_DM, HX_ZTSJ.F_CX_DJ_PZJGXX('ZZLX_DM', NSR.DJXH) ZZLX_DM, HX_ZTSJ.F_CX_DJ_PZJGXX('ZZHM', NSR.DJXH) ZZHM, HX_ZTSJ.F_CX_DJ_PZJGXX('KYSLRQ', NSR.DJXH) KYSLRQ, HX_ZTSJ.F_CX_DJ_PZJGXX('SCJYQXQ', NSR.DJXH) SCJYQXQ, HX_ZTSJ.F_CX_DJ_PZJGXX('SCJYQXZ', NSR.DJXH) SCJYQXZ, KZ.ZCDLXDH, KZ.SCJYDLXDH, KZ.FDDBRGDDH, KZ.FDDBRYDDH, KZ.BSRXM, KZ.BSRGDDH, KZ.BSRYDDH, KZ.CWFZRXM, KZ.CWFZRGDDH, KZ.CWFZRYDDH, NSR.FJMQYBZ, NSR.KQCCSZTDJBZ, NSR.YXBZ, NSR.LRR_DM, NSR.LRRQ, NSR.XGR_DM, NSR.XGRQ, NSR.NSRBM, NSR.SSDABH, NSR.SHXYDM, '联系信息' LXXX, (SELECT '受理信息' FROM DJ_YSQYWSLXXB SL WHERE NSR.DJXH = SL.DJXH AND ROWNUM = 1) SLXX, KZ.ZFJGLX_DM, (SELECT '总机构信息' FROM DJ_ZJGXX ZJG WHERE NSR.DJXH = ZJG.DJXH AND ROWNUM = 1) ZJGXX, (SELECT '分支机构信息' FROM DJ_FZJGXX FZ WHERE NSR.DJXH = FZ.DJXH AND ROWNUM = 1) FZJGXX, NSR.DJXH FROM DJ_NSRXX NSR, DJ_NSRXX_KZ KZ WHERE NSR.DJXH = KZ.DJXH AND NSR.ZGSWJ_DM IN (SELECT SWJG_DM FROM DM_GY_SWJG V START WITH V.SWJG_DM IN ('24301110000') CONNECT BY PRIOR V.SWJG_DM = V.SJSWJG_DM) AND (('Y' = 'N') OR ('N' = 'N' AND NSR.KZZTDJLX_DM <> '1600')) AND NSR.YXBZ IN ('Y') AND NSR.NSRMC LIKE '%"+ mc +"%' AND NSR.DJRQ >= TO_DATE('1971-12-01', 'YYYY-MM-DD')") 
        arr.append("footvalue=")
        arr.append("page=1")
        arr.append("start=0")
        limit = self.data['limit']
        body = "&".join(arr)
        body = urllib.quote(body,"='&")
        print body
        request.body = body