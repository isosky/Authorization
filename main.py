#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-2 15:56
# @Author  : wtr
# @File    : main.py

import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado.options import define, options
from auth_main import *

define("port", default=8878, help="run on the given port", type=int)
tornado.options.parse_command_line()

# websocket
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        return True

    def open(self):
        WebSocketHandler.waiters.add(self)
        print 'open'
        print self.waiters

    def on_close(self):
        WebSocketHandler.waiters.remove(self)

    @classmethod
    def pushdata(cls, message, app):
        s = datapipe(message)
        data = s.getdata()
        for i in cls.waiters:
            if i == app:
                i.write_message(data)

    def on_message(self, message):
        WebSocketHandler.pushdata(message, self)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocketHandler)
        ]

        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
