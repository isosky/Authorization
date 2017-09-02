#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-2 10:54
# @Author  : wtr
# @File    : db.py
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 09:39:20 2016

@author: sl
"""
import datetime
import os

import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado.options import define, options
from auth_main import *

define("port", default=8878, help="run on the given port", type=int)
tornado.options.parse_command_line()


class AjaxHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def post(self):
        lonlat = self.get_argument("message")
        timerange = self.get_argument("timerange")
        ret = None
        self.write(ret)

    def get(self):
        lonlat = self.get_argument("message")
        timerange = self.get_argument("timerange")
        ret = None
        self.write(ret)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/test", AjaxHandler)
        ]

        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
