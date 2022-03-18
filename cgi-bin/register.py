#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi, cgitb
import hashlib

import web
import mysql.connector

db = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="gravatar"
)
cursor = db.cursor()

def checkAvailable():
    pass


def checkUserExist(email):
    cursor.execute("SELECT * FROM user WHERE email=\"" + email + "\"")
    result = cursor.fetchall()  # fetchall() 获取所有记录
    if len(result) != 0:
        return True
    else:
        return False

def Insert(name, email, picture, password):
    flag = checkUserExist(email)
    if not flag:
        # 头像要先弄一个默认的，插入user表
        sql_user = "INSERT INTO user (username, email, profile_picture) VALUES (%s, %s, %s)"
        val_user = [(name, email, picture)]
        cursor.executemany(sql_user, val_user)

        user_id_sql = "SELECT id FROM user WHERE email=\"" + email + "\""
        cursor.execute(user_id_sql)
        user_id = [x[0] for x in cursor.fetchall()][0]

        # 需要对密码进行加密，插入密码表
        password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        sql_password = "INSERT INTO user_password (password, user_id) VALUES (%s, %s)"
        val_password = [(password, user_id)]
        cursor.executemany(sql_password, val_password)
        db.commit()
        return True
    else:
        return False



# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取数据
name = form.getvalue('name')
email  = form.getvalue('email')
password  = form.getvalue('password')
# 需要使用默认的头像
picture = "pictures/default.png"



print("Content-type:text/html")
print()
print(Insert(name, email, picture, password))


