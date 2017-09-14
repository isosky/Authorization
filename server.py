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
        # print self.waiters

    def on_close(self):
        WebSocketHandler.waiters.remove(self)

    @classmethod
    def pushdata(cls, message, app):
        for i in cls.waiters:
            if i == app:
                print message
                data = []
                temp = message.split(',')
                if temp[0] == 'initv':
                    data = initv()
                elif temp[0] == 'q_tree':
                    data = query_group_tree()
                elif temp[0] == 'q_g_r':
                    data = query_group_role()
                elif temp[0] == 'addgroup':
                    addgroup(temp[1], temp[2])
                    data = initv()
                    i.write_message(data)
                    data = query_group_tree()
                elif temp[0] == 'modifygroup':
                    modifygroup(temp[1], temp[2])
                    data = initv()
                    i.write_message(data)
                    data = query_group_tree()
                elif temp[0] == 'deletegroup':
                    if temp[2] == 'false':
                        status = False
                    else:
                        status = True
                    deletegroup(temp[1], status)
                    data = initv()
                    i.write_message(data)
                    data = query_group_tree()
                elif temp[0] == 'selectgroup':
                    gid = temp[1]
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'add_per':
                    per_name = temp[1]
                    add_per(per_name)
                    data = query_per_name()
                elif temp[0] == 'modify_per':
                    modifyper(temp[1], temp[2])
                    data = query_per_name()
                elif temp[0] == 'delete_per':
                    temp = message.split(',')[1]
                    deleteper(temp)
                    data = query_per_name()
                elif temp[0] == 'add_role_per':
                    r_id = temp[1]
                    p_id = temp[2]
                    addrole_per(r_id=r_id, p_id=p_id)
                    gid = temp[3]
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'delete_role_per':
                    r_id = temp[1]
                    p_id = temp[2]
                    deleterole_per(r_id=r_id, p_id=p_id)
                    gid = temp[3]
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'add_role':
                    gid = temp[1]
                    addrole(gid, temp[2])
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'modify_role':
                    gid = temp[3]
                    modifyrole(temp[1], temp[2])
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'delete_role':
                    gid = temp[2]
                    deleterole(temp[1])
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'role_add_user':
                    addrole_user(r_id=temp[1], user_id=temp[2])
                    gid = temp[3]
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                elif temp[0] == 'role_delete_user':
                    deleterole_user(r_id=temp[1], user_id=temp[2])
                    gid = temp[3]
                    data = initv()
                    i.write_message(data)
                    data = query_group_role(gid)
                    i.write_message(data)
                    data = query_group_user(gid)
                    i.write_message(data)
                    data = query_per_name()
                if data:
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
