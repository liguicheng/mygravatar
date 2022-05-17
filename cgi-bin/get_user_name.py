#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import os
import jwt
import MySQL
import json


def get_user_name(email):
    cursor.execute("SELECT username FROM user WHERE email=%s", (email,))
    result = cursor.fetchall()  # fetchall() 获取所有记录
    return result


db_conn = MySQL.MySQLConn()
cursor = db_conn.get_cursor()

email  = ""
name = ""
token = ""

if "HTTP_COOKIE" in os.environ:
    # email_cookie = os.environ["HTTP_COOKIE"].split(';')[0]
    #email_cookie = os.environ["HTTP_COOKIE"]
    cookies = os.environ["HTTP_COOKIE"].split(';')
    for cookie in cookies:
        key, value = cookie.split("=")
        key = key.strip()
        value = value.strip()
        if key == 'token':
            token = value
    # email_cookie = cookies[1].split('=')[0]

# 对token解码，校验是不是对应的email
if token == "":
    email = ""
else:
    try:
        val = jwt.decode(token, 'lgc12345', issuer='lgc',  algorithms=['HS256'])
        email = val['data']['email']
        result = get_user_name(email)
        name = [x[0] for x in result][0]
    except:
        # 解码出错的话就获取不了用户名（即为空字符串），这里不做操作，前端获取到的用户名是空字符串则返回登录界面
        pass

data = {
    "name": name,
    "email": email
}

print("Content-type:application/json;charset=UTF-8;")
# print("Set-Cookie: name=" + name)
print()
print(json.dumps(data))


# print(pic)
# 头像，如果没设置，则使用默认的
