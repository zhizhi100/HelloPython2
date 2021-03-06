# encoding: utf-8
'''
Created on 2015-10-12

@author: ZhongPing
'''
from datetime import date
 
__doc__ = """Golden Proxy.
  
This is modified based of TinyHTTPProxy version 0.3.1.
  
2015/10/30 - Modified by zhongping
             * Delete FTP support
             * Delete daemon support
"""
  
__version__ = "0.4.0"
  
import BaseHTTPServer, select, socket, SocketServer, urlparse
import logging
import logging.handlers
import getopt
import sys
import os
import signal
import threading
from types import FrameType, CodeType
from time import sleep
import ProxyConfig
import RuleMatch
import gt.license.auth as auth
import gt.license.trial as trial
import random
from gt.gtcore.env import Gtenv,gtdir
import ConfigParser
  
DEFAULT_LOG_FILENAME = "proxy.log"

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle
  
    server_version = "GoldenProxy/" + __version__
    rbufsize = 0                        # self.rfile Be unbuffered
    
    def _getwebtime(self,url):
        import urllib2
        from datetime import datetime
        send_header = {"If-Modified-Since":"q" }
        req = urllib2.Request(url,headers=send_header)
        r = urllib2.urlopen(req)
        receive_header = r.info()
        nowdate = datetime.strptime(receive_header["Date"], "%a, %d %b %Y %X %Z")
        da = nowdate.strftime('%Y%m%d')
        now = datetime.now()
        db = now.strftime('%Y%m%d')
        return da == db
  
    def handle(self):
        myenv = Gtenv("")
        if myenv.istrial:            
            rand = random.randint(0,100)
            if rand == 90:                
                licdays,licdate = trial.haskey()
                if licdays == 0 or (licdate - date.today()).days < 0:
                    self.server.logger.warning('试用授权到期或没有正式授权文件，系统启动失败！')
                    myenv.running = False
                    return
        else:
            rand = random.randint(0,1000)
            if rand == 90:
                licdays,licdate = auth.haslic()
                if licdays == 0 or (licdate - date.today()).days < 0:
                    self.server.logger.warning('试用授权到期或没有正式授权文件，系统启动失败！')
                    myenv.running = False
                    return

        (ip, port) =  self.client_address
        self.server.logger.log (logging.INFO, "Request from '%s'", ip)
        if hasattr(self, 'allowed_clients') and ip not in self.allowed_clients:
            self.raw_requestline = self.rfile.readline()
            if self.parse_request(): self.send_error(403)
        else:
            try:self.__base_handle()
            except socket.error, arg:
                try: msg = arg[1]
                except: msg = arg
                self.send_error(404, msg)
                self.server.logger.log(logging.ERROR,'Exception happened during processing'+\
                                       ',error info:'+msg) 
  
    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i+1:])
        else:
            host_port = netloc, 80
        self.server.logger.log (logging.INFO, "connect to %s:%d", host_port[0], host_port[1])
        try: soc.connect(host_port)
        except socket.error, arg:
            try: msg = arg[1]
            except: msg = arg
            self.send_error(404, msg)
            return 0
        return 1
  
    def do_CONNECT(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                self.log_request(200)
                self.wfile.write(self.protocol_version +
                                 " 200 Connection established\r\n")
                self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        finally:
            soc.close()
            self.connection.close()
  
    def do_GET(self):
        rand = random.randint(0,1000)
        myenv = Gtenv("")
        if rand == 90 or not myenv.checked:
            if self.path != 'http://www.google.com/_gtool_/GoldenToolProxy.html':
                if not self._getwebtime(self.path):
                    self.server.logger.warning('本地时间与系统时间冲突，系统启动失败！')
                    myenv.running = False
                    return
                myenv.checked = True
                    
        if self.path=='http://www.gtool.com/stopproxy?key=79798798':
            #self.server.close()
            print self.path
            self.server.logger.warning('your proxy server to be closed soon')
            self.wfile.write('your proxy server to be closed soon')
            myenv.running = False
            self.server.close_connection = True
            #self.server.shutdown()
            #self.server.stop()
            return
        #0 get request accept type,now set it to *
        '''  I can't sure,guess that the Accept tag is not useful
        accepttype = self.headers.get('Accept')
        if accepttype:
            if accepttype == '*/*':
                accepttype = '*'
            elif accepttype.find('text/html') == 0:
                accepttype = 'html'
            else:
                accepttype = 'other'
        else:
            accepttype = '*'
        '''
        accepttype = '*'
        #1 deal with redirect rules, FTP may raise error
        (needredirect,redirectedpath) = self.rulehandler.redirect(self.path,accepttype)
        if needredirect:
            self.headers['Gtool_url'] = self.path
            self.server.logger.log(logging.WARN,'Reditrected!From['+self.path+'] to ['+redirectedpath +']')
            self.path = redirectedpath
        #finished the redirect
        
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        #do not support ftp protecl
        if scm not in ('http', 'noftp') or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        #print self.headers
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if scm == 'http':
                if self._connect_to(netloc, soc) :
                    #self.log_request()
                    soc.send("%s %s %s\r\n" % (self.command,
                                               urlparse.urlunparse(('', '', path,
                                                                    params, query,
                                                                    '')),
                                               self.request_version))
                    self.headers['Connection'] = 'close'
                    del self.headers['Proxy-Connection']
                    #del self.headers['content-length']
                    for key_val in self.headers.items():
                        soc.send("%s: %s\r\n" % key_val)
                    soc.send("\r\n")
                    if not(needredirect):
                        (ismodified,errmsg,resp) = self.rulehandler.modify(self.path,accepttype,self.headers)
                        if ismodified:
                            self.server.logger.log(logging.WARN,'Modified! path:['+self.path+']')
                            self._write_modifiedtext(resp)
                        else:
                            if not(errmsg ==''):self.server.logger.log (logging.ERROR,'Exception happened during of Modify ['\
                                                                        + self.path + '],error msg:'+errmsg)
                            self._read_write(soc)
                    else:
                        self._read_write(soc)
            elif scm == 'ftp':
                # fish out user and password information
                pass
        finally:
            soc.close()
            self.connection.close()
  
    def _read_write(self, soc, max_idling=20, local=False):
        iw = [self.connection, soc]
        local_data = ""
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 1)
            if exs: break
            if ins:
                for i in ins:
                    if i is soc: out = self.connection
                    else: out = soc
                    data = i.recv(8192)
                    if data:
                        if local: local_data += data
                        else: out.send(data)
                        count = 0
            if count == max_idling: break
        if local: return local_data
        return None
    
    def _write_modifiedtext(self,r):
        code = r['code']
        self.send_response(code)
        receive_header = r['header']
        for key,val in receive_header.items():
            if val != 'gzip':
                self.send_header(key,val)
        self.end_headers()
        html = r['html'] 
        self.wfile.write("\r\n")
        self.wfile.write()
        self.wfile.write(html)
        self.wfile.write("\r\n0000\r\n\r\n")
      
    def do_POST(self):      
        oldpath = self.path
        (needrepost,repostpath) = self.rulehandler.repost(self.path,'*')
        if needrepost:  
            self.server.logger.log(logging.WARN,'Reposted!From['+self.path+'] to ['+repostpath +']')
            self.path = repostpath
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        #do not support ftp protecl
        if scm not in ('http', 'noftp') or fragment or not netloc:
            self.send_error(400, "bad url %s" % self.path)
            return
        #print self.headers
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if scm == 'http':
                if self._connect_to(netloc, soc) :
                    #self.log_request()
                    soc.send("%s %s %s\r\n" % (self.command,
                                               urlparse.urlunparse(('', '', path,
                                                                    params, query,
                                                                    '')),
                                               self.request_version))
                    self.headers['Connection'] = 'close'
                    if needrepost:
                        self.headers['Gtool_url'] = oldpath             
                    del self.headers['Proxy-Connection']
                    for key_val in self.headers.items():
                        soc.send("%s: %s\r\n" % key_val)
                    soc.send("\r\n")
                    self._read_write(soc)
            elif scm == 'ftp':
                # fish out user and password information
                pass
        finally:
            soc.close()
            self.connection.close()
    
    do_HEAD = do_GET
    #do_POST = do_GET
    do_PUT  = do_GET
    do_DELETE=do_GET
  
    def log_message (self, format, *args):
        self.server.logger.log (logging.INFO, "%s %s", self.address_string (),
                                format % args)
  
    def log_error (self, format, *args):
        self.server.logger.log (logging.ERROR, "%s %s", self.address_string (),
                                format % args)
  
class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer):
    def __init__ (self, server_address, RequestHandlerClass, logger=None):
        BaseHTTPServer.HTTPServer.__init__ (self, server_address,
                                            RequestHandlerClass)
        self.logger = logger
  
def logSetup (filename, log_size, daemon):
    logger = logging.getLogger ("Golden Proxy")
    logger.setLevel (logging.WARN)

    if not filename:
        if not daemon:
            # display to the screen
            handler = logging.StreamHandler ()
        else:
            handler = logging.handlers.RotatingFileHandler (DEFAULT_LOG_FILENAME,
                                                            maxBytes=(log_size*(1<<16)),
                                                            backupCount=5)
    else:
        handler = logging.handlers.RotatingFileHandler (filename,
                                                        maxBytes=(log_size*(1<<16)),
                                                        backupCount=5)
    fmt = logging.Formatter ("[%(asctime)-12s.%(msecs)03d] "
                             "%(levelname)-8s {%(name)s %(threadName)s}"
                             " %(message)s",
                             "%Y-%m-%d %H:%M:%S")
    handler.setFormatter (fmt)
    
    console = logging.StreamHandler()
    console.setLevel(logging.WARN)
    console.setFormatter (fmt)
    logger.addHandler(console)
  
    handler.setLevel(logging.WARN)
    logger.addHandler (handler)
    return logger
  
def usage (msg=None):
    if msg: print msg
    print sys.argv[0], "[-p port] [-l logfile] [-dh] [allowed_client_name ...]]"
    print
    print "   -p       - Port to bind to"
    print "   -l       - Path to logfile. If not specified, STDOUT is used"
    print "   -d       - Run in the background"
    print
  
def handler (signo, frame):
    while frame and isinstance (frame, FrameType):
        if frame.f_code and isinstance (frame.f_code, CodeType):
            if "run_event" in frame.f_code.co_varnames:
                frame.f_locals["run_event"].set ()
                return
        frame = frame.f_back

def main ():
    path = sys.path[0]
    if os.path.isfile(path):
        path = os.path.dirname(path)
    #path = "F:\\release"
    gtdir = path
    myenv = Gtenv(path) 
    path = myenv.getpath() 
    cfgfile = path + '/config.json'
    logfile = ""
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(path + "/service.ini")
        logfile = path + "/" + cf.get("log","proxy")
    except Exception as e:
        pass    
    if logfile == '':
        logfile = path + '/proxy.log'
    daemon  = False
    max_log_size = 2
    port = 8000
    allowed = []
    run_event = threading.Event ()
    local_hostname = socket.gethostname ()
    
    '''
  
    try: opts, args = getopt.getopt (sys.argv[1:], "l:dhp:", [])
    except getopt.GetoptError, e:
        usage (str (e))
        return 1
  
    for opt, value in opts:
        if opt == "-c": cfgfile = value
        if opt == "-p": port = int (value)
        if opt == "-l": logfile = value
        if opt == "-d": daemon = not daemon
        if opt == "-h":
            usage ()
            return 0
            
    '''
  
    # setup the log file
    logger = logSetup (logfile, max_log_size, daemon)
    
    #logger.info("a..........")
    
    licdays,licdate = trial.haskey()
    if licdays == 0 or (licdate - date.today()).days < 0:
        licdays,licdate = auth.haslic()
        if licdays == 0 or (licdate - date.today()).days < 0:
            logger.warning('试用授权到期或没有正式授权文件，系统启动失败！')
            return 0
        else:
            myenv.istrial = False
            myenv.licdate = licdate
    else:
        myenv.istrial = True
        myenv.licdate = licdate
    if daemon:
        pass
        #daemonize (logger)
    #signal.signal (signal.SIGINT, handler) #必须屏蔽
    #logger.info("b..........")
  
    '''
    if args:
        allowed = []
        for name in args:
            client = socket.gethostbyname(name)
            allowed.append(client)
            logger.log (logging.INFO, "Accept: %s (%s)" % (client, name))
        ProxyHandler.allowed_clients = allowed
    else:
        logger.log (logging.WARNING, "Any clients will be served...")
    '''
        
    cfgcls = ProxyConfig.config(cfgfile)
    cfg = {}
    (cfg['Redirect'],cfg['Modify'],cfg['Repost']) = cfgcls.read()
    ProxyHandler.config = cfg
    
    rulematch = RuleMatch.RuleMatch(cfg['Redirect'],cfg['Modify'],cfg['Repost'])
    ProxyHandler.rulehandler = rulematch
  
    #server_address = (socket.gethostbyname (local_hostname), port)
    server_address = ('127.0.0.1', port)
    ProxyHandler.protocol = "HTTP/1.0"
    httpd = ThreadingHTTPServer (server_address, ProxyHandler, logger)
    sa = httpd.socket.getsockname ()
    logger.warning("Servering HTTP Proxy on %s port %s", sa[0], sa[1])
    req_count = 0
    myenv.running = True
    myenv.checked = False
    while myenv.running and not run_event.isSet ():
        try:
            httpd.handle_request ()
            req_count += 1
            if req_count == 1000:
                logger.log (logging.INFO, "Number of active threads: %s",
                            threading.activeCount ())
                req_count = 0
            if not myenv.running:
                httpd.__is_shut_down = True
        except select.error, e:
            if e[0] == 4: pass
            else:
                logger.log (logging.CRITICAL, "Errno: %d - %s", e[0], e[1])
    logger.log (logging.WARNING, "Server shutdown")
    
    return 0
  
if __name__ == '__main__':
    #sys.exit (main ())
    main()