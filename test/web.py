# encoding: utf-8
'''
Created on 2015年11月3日

@author: ZhongPing
'''
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options 

class Hello(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")
        
settings = {
            "static_path": "static",
}

app = tornado.web.Application([
    (r"/", Hello),
    ],**settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8001)
    tornado.ioloop.IOLoop.instance().start()

