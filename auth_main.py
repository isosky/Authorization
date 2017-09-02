#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-2 10:55
# @Author  : wtr
# @File    : auth_main.py

from  db import dbc
import time


def addgroup(g_id, g_f_id, g_name):
    db = dbc()
    try:
        temp_sql = "INSERT INTO auth_group (g_id, g_f_id, group_name) VALUES (%s,%s,'%s')"%(g_id, g_f_id, g_name)
        db.cur.execute(temp_sql)
    except Exception as err:
        print(err)
    db.commit()


def modifygroup(g_id, g_f_id, g_name):
    db = dbc()
    try:
        temp_sql = "UPDATE auth_group SET (g_f_id,group_name)=(%s,'%s') WHERE g_id=%s"%(g_f_id, g_name, g_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print(err)
    db.commit()


def deletegroup(g_id):
    db = dbc()
    try:
        temp_sql = "DELETE from  auth_group  WHERE g_id=%s"%g_id
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def addrole(r_id, g_id, r_name):
    db = dbc()
    try:
        temp_sql = "INSERT INTO auth_role_group (r_id, g_id, role_name) VALUES (%s,%s,'%s')"%(r_id, g_id, r_name)
        db.cur.execute(temp_sql)
    except Exception as err:
        print(err)
    db.commit()


def modifyrole(r_id, g_id, r_name):
    db = dbc()
    try:
        temp_sql = "UPDATE auth_role_group SET (g_id,role_name)= (%s,'%s') where r_id=%s"%(g_id, r_name, r_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print(err)
    db.commit()


def deleterole(r_id):
    db = dbc()
    try:
        temp_sql = "DELETE from  auth_role_group  WHERE r_id=%s"%r_id
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def adduser(g_id, r_id, user_name):
    db = dbc()
    db.cur.execute('SELECT max(user_id) FROM auth_user')
    max_id = db.cur.fetchone()[0] + 1
    try:
        temp_sql = "INSERT INTO auth_user (user_id, g_id, r_id, user_name, isroot,login_name,pwd) VALUES (%s,%s,%s,'%s',%s,'%s','%s')"%(
            max_id, g_id, r_id, user_name, False, 'lcf', None)
        print  temp_sql
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def modifyuser(user_id, g_id, r_id, u_name):
    db = dbc()
    try:
        temp_sql = "Update auth_user set (g_id,r_id,user_name) = (%s,%s,'%s') WHERE user_id=%s"%(
            g_id, r_id, u_name, user_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def updatepwd(user_id, pwd):
    # todo 验证
    db = dbc()
    try:
        temp_sql = "Update auth_user set pwd = '%s' WHERE user_id=%s"%(pwd, user_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def deleteuser(user_id):
    db = dbc()
    try:
        temp_sql = "Delete from auth_user WHERE  user_id=%s"%user_id
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def adduser_per(user_id, p_id):
    db = dbc()
    try:
        temp_sql = "Insert into auth_user_per VALUES (%s,%s)"%(user_id, p_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def addrole_per(r_id, p_id):
    db = dbc()
    try:
        temp_sql = "Insert into auth_role_per VALUES (%s,%s)"%(r_id, p_id)
        db.cur.execute(temp_sql)
        # 对这个角色的每个员工增加这个权限
        # 一个人只有一个角色
        temp_sql = 'select user_id from auth_user where r_id=%s'%r_id
        db.cur.execute(temp_sql)
        all_user = db.cur.fetchall()
        for user in all_user:
            adduser_per(user_id=user, p_id=p_id)
    except Exception as err:
        print err
    db.commit()


def addgroup_per(g_id, p_id):
    db = dbc()
    try:
        temp_sql = "Insert into auth_group_per VALUES (%s,%s)"%(g_id, p_id)
        db.cur.execute(temp_sql)
        # 对这个部门的每个员工增加这个权限
        temp_sql = 'select user_id from auth_user where g_id=%s'%g_id
        db.cur.execute(temp_sql)
        all_user = db.cur.fetchall()
        for user in all_user:
            adduser_per(user_id=user, p_id=p_id)
    except Exception as err:
        print err
    db.commit()


def deleteuser_per(user_id, p_id):
    db = dbc()
    try:
        temp_sql = "delete from auth_user_per where user_id=%s and p_id=%s"%(user_id, p_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def deleterole_per(r_id, p_id):
    db = dbc()
    try:
        temp_sql = "delete from auth_role_per where r_id=%s and p_id=%s"%(r_id, p_id)
        db.cur.execute(temp_sql)
        # 对这个角色的每个员工删除权限
        temp_sql = "select * from auth_user WHERE  r_id=%s"%r_id
        db.cur.execute(temp_sql)
        all_user = db.cur.fetchall()
        for user in all_user:
            deleteuser_per(user_id=user, p_id=p_id)
    except Exception as err:
        print err
    db.commit()


def deletegroup_per(g_id, p_id):
    db = dbc()
    try:
        temp_sql = "delete from auth_group_per where g_id=%s and p_id=%s"%(g_id, p_id)
        db.cur.execute(temp_sql)
        # 对这个部门的每个员工删除权限
        temp_sql = "select * from auth_user WHERE  g_id=%s"%g_id
        db.cur.execute(temp_sql)
        all_user = db.cur.fetchall()
        for user in all_user:
            deleteuser_per(user_id=user, p_id=p_id)
    except Exception as err:
        print err
    db.commit()


if __name__ == '__main__':
    adduser(1, 3, "李晨放")
    # deletegroup(5)
