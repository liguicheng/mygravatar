#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import base64
import cgi
import os
import jwt
import MySQL


def get_profile_pic(email):
    cursor.execute("SELECT profile_picture FROM user WHERE email=%s", (email,))
    return cursor.fetchall()  # fetchall() 获取所有记录


# 返回base64编码
def get_user_pic(pic_url):
    pic = open(pic_url, "rb")
    pic_code = base64.b64encode(pic.read())
    pic.close()

    pic_code = "data:image/" + str(pic_url).split('.')[-1] + ";base64," + bytes.decode(pic_code)

    return pic_code


db_conn = MySQL.MySQLConn()
cursor = db_conn.get_cursor()

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

email  = form.getvalue('email')
token = ""
token_email = ""

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
    print("Content-type:text/html")
    print()
else:
    try:
        val = jwt.decode(token, 'lgc12345', issuer='lgc',  algorithms=['HS256'])
        token_email = val['data']['email']
        # 校验邮箱
        if token_email == email:
            # 获取头像路径
            result = get_profile_pic(email)
            pic_url = [x[0] for x in result][0]

            # getUserPic根据邮箱获取头像
            code = get_user_pic(pic_url)

            print("Content-type:text/html")
            print()
            print(code)
        else:
            print("Content-type:text/html")
            print()
    except:
        print("Content-type:text/html")
        print()




