#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import base64
import cgi, cgitb

import mysql.connector


def getProfilePic(email):
    cursor.execute("SELECT profile_picture FROM user WHERE email=\"" + email + "\"")
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

# 获取头像路径
email  = form.getvalue('email')
result = getProfilePic(email)
pic_url = [x[0] for x in result][0]


print("Content-type:text/html")
print()
print(pic_url)