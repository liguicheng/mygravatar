#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi, cgitb
import hashlib

import mysql.connector
import datetime


def checkUserExist(email):
    cursor.execute("SELECT * FROM user WHERE email=\"" + email + "\"")
    result = cursor.fetchall()  # fetchall() 获取所有记录
    if len(result) != 0:
        return True
    else:
        return False

def checkPassword(email, password):
    # 需要把密码加密了，然后看与数据库中加密后的密码一样不
    user_id_sql = "SELECT id FROM user WHERE email=\"" + email + "\""
    cursor.execute(user_id_sql)
    # 获取从数据库中选出的数据
    user_id = [x[0] for x in cursor.fetchall()][0]

    password_encode = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    sql_password = "SELECT password FROM user_password WHERE user_id=\"" + str(user_id) + "\""
    cursor.execute(sql_password)
    user_password = [x[0] for x in cursor.fetchall()][0]
    if password_encode == user_password:
        return True
    else:
        return False



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
password  = form.getvalue('password')

# 身份过期时间为一天
expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=24*60*60), "%a, %d-%b-%Y %H:%M:%S GMT")


print("Content-type:text/html")
print("Set-Cookie: email=" + email + ";expires=" + expires)
print()
if not checkUserExist(email):
    print("NOT_EXIST")
else:
    print(checkPassword(email, password))
# print(email)
# 登录之后应该要设置cookie，以及前端界面的样子
# 头像，如果没设置，则使用默认的
