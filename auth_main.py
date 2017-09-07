#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-9-2 10:55
# @Author  : wtr
# @File    : auth_main.py

from  db import dbc
import time
import json
import random

def random10():
    seed = "qwertyuiopasdfghjklzxcvbnm"
    sa = []
    for i in range(10):
        sa.append(random.choice(seed))
    sa = "".join(sa)
    return sa

def addgroup(g_f_id, g_name):
    db = dbc()
    # todo auth_group
    db.cur.execute('SELECT max(g_id) FROM auth_group')
    max_id = db.cur.fetchone()[0] + 1
    try:
        temp_sql = "INSERT INTO auth_group (g_id, g_f_id, group_name) VALUES (%s,%s,'%s')"%(max_id, g_f_id, g_name)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def modifygroup(g_id, g_name):
    db = dbc()
    try:
        temp_sql = "UPDATE auth_group SET group_name='%s' WHERE g_id=%s"%(g_name, g_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


# todo waiting for testing
def deletegroup(g_id, delete_sub):
    db = dbc()
    if delete_sub:
        try:
            temp_sql = 'select g_id from auth_group where g_f_id= %s'%g_id
            db.cur.execute(temp_sql)
            d_gids = db.cur.fetchall()
            for gid in d_gids:
                if checksub(gid):
                    for temp in checksub(g_id):
                        deletegroup(gid, True)
                else:
                    deletegroup(gid, False)
        except Exception as err:
            print err
    else:
        try:
            temp_sql = "select user_id from auth_user where g_id=%s"%g_id
            db.cur.execute(temp_sql)
            if db.cur.rowcount > 1:
                for user_id in db.cur.fetchall():
                    deleteuser(user_id=user_id)
            temp_sql = "select r_id from auth_role_group where g_id=%s"%g_id
            db.cur.execute(temp_sql)
            if db.cur.rowcount > 1:
                for role_id in db.cur.fetchall():
                    deleterole(r_id=role_id)
            temp_sql = "DELETE from  auth_group  WHERE g_id=%s"%g_id
            db.cur.execute(temp_sql)
        except Exception as err:
            print err
    db.commit()


def checksub(g_id):
    db = dbc()
    try:
        temp_sql = 'select g_id from auth_group where g_f_id= %s'%g_id
        db.cur.execute(temp_sql)
        if db.cur.rowcount > 1:
            d_gids = db.cur.fetchall()
            return list(x[0] for x in d_gids)
        else:
            return False
    except Exception as err:
        print err


def addrole(g_id, r_name):
    db = dbc()
    # todo auth_role_group为空的时候
    db.cur.execute('SELECT max(r_id) FROM auth_role_group')
    max_id = db.cur.fetchone()[0] + 1
    try:
        temp_sql = "INSERT INTO auth_role_group (r_id, g_id, role_name) VALUES (%s,%s,'%s')"%(max_id, g_id, r_name)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def modifyrole(r_id, g_id, r_name):
    db = dbc()
    try:
        temp_sql = "UPDATE auth_role_group SET (g_id,role_name)= (%s,'%s') where r_id=%s"%(g_id, r_name, r_id)
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def deleterole(r_id):
    db = dbc()
    try:
        temp_sql = "select p_id from auth_role_per where r_id = %s"%r_id
        db.cur.execute(temp_sql)
        if db.cur.rowcount > 1:
            for temp in db.cur.fetchall():
                deleterole_per(r_id, temp[0])
            db.commit()
        temp_sql = "DELETE from  auth_role_group  WHERE r_id=%s"%r_id
        db.cur.execute(temp_sql)
    except Exception as err:
        print err
    db.commit()


def adduser(g_id, r_id, user_name):
    db = dbc()
    # todo user表为空的时候的判断
    db.cur.execute('SELECT max(user_id) FROM auth_user')
    max_id = db.cur.fetchone()[0] + 1
    try:
        temp_sql = "INSERT INTO auth_user (user_id, g_id, r_id, user_name, isroot,login_name,pwd) VALUES (%s,%s,%s,'%s',%s,'%s','%s')"%(
            max_id, g_id, r_id, user_name, False, 'lcf', None)
        # print  temp_sql
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
        temp_sql = "select p_id from auth_user_per where user_id = %s"%user_id
        db.cur.execute(temp_sql)
        if db.cur.rowcount > 1:
            for temp in db.cur.fetchall():
                deleteuser_per(user_id, temp[0])
            db.commit()
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


def query_group_tree():
    db = dbc()
    temp = {}
    temp[0] = get_sub(0, db)
    # print temp
    return json.dumps({'name': 'q_tree', 'data': temp})


def get_sub(root, db):
    temp_sql = 'select g_id from auth_group where g_f_id=%s'%root
    db.cur.execute(temp_sql)
    r = {}
    if db.cur.rowcount > 0:
        temp = db.cur.fetchall()
        if type(root) != int:
            r[root[0]] = {}
        else:
            r[root] = {}
        for i in temp:
            r[root][i[0]] = get_sub(i[0], db)
        return r[root]


def query_group_user(g_id):
    db = dbc()
    temp_sql = 'select user_id,user_name,r_id from auth_user where g_id=%s ORDER BY user_id'%g_id
    try:
        db.cur.execute(temp_sql)
        if db.cur.rowcount > 0:
            temp = list(db.cur.fetchall())
            temp = [list(x) for x in temp]
            return json.dumps({'name': 'user_list', 'data': list(temp)})
        else:
            return json.dumps({'name': 'user_list', 'data': []})
    except Exception as err:
        print err


def query_group_role(g_id):
    db = dbc()
    try:
        temp_sql = "select r_id,role_name from auth_role_group where g_id=%s ORDER BY r_id"%g_id
        db.cur.execute(temp_sql)
        if db.cur.rowcount > 0:
            temp = db.cur.fetchall()
            return json.dumps({'name': 'role_list', 'data': list(temp)})
        else:
            return json.dumps({'name': 'role_list', 'data': []})
    except Exception as err:
        print err


def initv():
    g_name = query_group_name()
    r_name = query_role_name()
    return json.dumps({'name': 'v', 'g_name': g_name, 'r_name': r_name})


def query_group_name():
    db = dbc()
    try:
        temp_sql = "SELECT g_id,group_name FROM auth_group ORDER BY g_id"
        db.cur.execute(temp_sql)
        temp = db.cur.fetchall()
        temp = list([list(x) for x in temp])
        return temp
    except Exception as err:
        print err


def query_role_name():
    db = dbc()
    try:
        temp_sql = "SELECT r_id,role_name FROM auth_role_group ORDER BY r_id"
        db.cur.execute(temp_sql)
        temp = db.cur.fetchall()
        temp = list([list(x) for x in temp])
        return temp
    except Exception as err:
        print err


if __name__ == '__main__':
    # print get_sub_tree(2, db)
    # print query_group_role(1)
    # query_group_tree()
    pass
    # deleterole(1)
    # r_g_id =[1,2,3,4]
    # for i in range(30):
    #     u_name =random10()
    #     r_id =random.choice(r_g_id)
    #     adduser(1,r_id,u_name)
