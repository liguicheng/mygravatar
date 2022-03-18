#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import base64
import cgi, cgitb

import mysql.connector
import os
import os


def getProfilePic(email):
    cursor.execute("SELECT profile_picture FROM user WHERE email=\"" + email + "\"")
    result = cursor.fetchall()  # fetchall() 获取所有记录
    return result

# 返回base64编码
def getUserPic(pic_url):
    pic = open(pic_url, "rb")
    pic_code = base64.b64encode(pic.read())
    pic.close()

    pic_code = "data:image/" + str(pic_url).split('.')[-1] + ";base64," + bytes.decode(pic_code)

    return pic_code


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

# getUserPic根据邮箱获取头像
code = getUserPic(pic_url)


print("Content-type:text/html")
print()
print(code)

# print(pic)
# 登录之后应该要设置cookie，以及前端界面的样子
# 头像，如果没设置，则使用默认的
