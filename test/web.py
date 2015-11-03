# encoding: utf-8
'''
Created on 2015年11月3日

@author: ZhongPing
'''
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web

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
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

