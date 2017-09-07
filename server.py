#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-4 10:03
# @Author  : wtr
# @File    : server.py

import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado.options import define, options
from auth_main import *

import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado.options import define, options
from auth_main import *

define("port", default=9909, help="run on the given port", type=int)
tornado.options.parse_command_line()


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
        for i in cls.waiters:
            if i == app:
                print message
                if message == 'initv':
                    data = initv()
                if message == 'q_tree':
                    data = query_group_tree()
                if message == 'q_g_r':
                    data = query_group_role()
                if 'addgroup' in message:
                    temp = message.split(',')
                    addgroup(temp[1], temp[2])
                    data = initv()
                    i.write_message(data)
                    data = query_group_tree()
                if 'modifygroup' in message:
                    temp = message.split(',')
                    modifygroup(temp[1], temp[2])
                    data = initv()
                    i.write_message(data)
                    data = query_group_tree()
                if 'deletegroup' in message:
                    temp = message.split(',')
                    if temp[2] == 'false':
                        status = False
                    else:
                        status = True
                    print status
                    # modifygroup(temp[1], temp[2])
                    data = initv()
                    # i.write_message(data)
                    # data = query_group_tree()
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
