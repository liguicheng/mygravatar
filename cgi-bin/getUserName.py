#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi, cgitb
import os

import mysql.connector
import json

from mysql.connector import Date


def getUserName(email):
    cursor.execute("SELECT username FROM user WHERE email=\"" + email + "\"")
    result = cursor.fetchall()  # fetchall() 获取所有记录
    return result

db = mysql.connector.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="gravatar"
)
cursor = db.cursor()

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取数据
email  = form.getvalue('email')
result = getUserName(email)
name = [x[0] for x in result][0]

if "HTTP_COOKIE" in os.environ:
    # email_cookie = os.environ["HTTP_COOKIE"].split(';')[0]
    #email_cookie = os.environ["HTTP_COOKIE"]
    cookies = os.environ["HTTP_COOKIE"].split(';')
    for cookie in cookies:
        key, value = cookie.split("=")
        key = key.strip()
        value = value.strip()
        if key == 'email':
            email_cookie = value
    # email_cookie = cookies[1].split('=')[0]

data = {
    "name": name,
    "email": email_cookie
}


print("Content-type:application/json;charset=UTF-8;")
# print("Set-Cookie: name=" + name)
print()
print(json.dumps(data))


# print(pic)
# 登录之后应该要设置cookie，以及前端界面的样子
# 头像，如果没设置，则使用默认的
