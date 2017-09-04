#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-2 10:54
# @Author  : wtr
# @File    : db.py
# -*- coding: utf-8 -*-


import psycopg2


class dbc(object):
    def __init__(self, s=True):
        self.conn = psycopg2.connect(database="authorization", user="postgres",
                                     password="123", host="localhost", port="5432")
        self.cur = self.conn.cursor()

    def disconnectdb(self):
        self.cur.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()