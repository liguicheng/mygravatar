#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi
import MySQL


def get_profile_pic(email):
    cursor.execute("SELECT profile_picture FROM user WHERE email=%s", (email, ))
    result = cursor.fetchall()  # fetchall() 获取所有记录
    return result


db_conn = MySQL.MySQLConn()
cursor = db_conn.get_cursor()

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取头像路径
email  = form.getvalue('email')
result = get_profile_pic(email)
pic_url = [x[0] for x in result][0]

print("Content-type:text/html")
print()
print(pic_url)