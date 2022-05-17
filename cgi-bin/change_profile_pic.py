#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import base64
import cgi
import hashlib
import os
import time
import jwt
import MySQL


def change_pic(base64URL, email):
    pic_type = base64URL.split(';')[0].split('/')[1]
    code = base64URL.split(',')[1]

    pic_data = base64.b64decode(code)

    # email路径加密，不是为了不让人破解，只是为了不明显地显示email值
    email_encode = hashlib.md5(email.encode(encoding='UTF-8')).hexdigest()
    pic_url = "pictures/" + email_encode + '.' + pic_type
    pic = open(pic_url, "wb")
    pic.write(pic_data)
    pic.close()

    # 把图片路径存到数据库
    return pic_url


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

# 获取数据
image  = form.getvalue('image')
email  = form.getvalue('email')
form_token  = form.getvalue('token')

token_email = ""
token = ""

# 需要进行身份校验，确认是该邮箱的用户才将头像换掉，通过cookie中存储的token，判断token中的个人信息，且判断token是否过期
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

# 防止csrf攻击，校验表单提交的cookie值是否符合要求
if token != "" and token != form_token:
    print("Content-type:text/html")
    print()
else:
    # 对token解码，校验是不是对应的email以及token是否过期
    if token == "":
        token_email = ""
    else:
        try:
            val = jwt.decode(token, 'lgc12345', issuer='lgc',  algorithms=['HS256'])
            # 判断token是否过期
            if val['exp'] < time.time():
                token_email = ""
            else:
                token_email = val['data']['email']
        except:
            token_email = ""

    # 判断token中的email是否与需要修改头像的email一致，身份校验
    if email == token_email:
        # changeUserPic更改头像
        pic_url = change_pic(image, email)
        sql = "UPDATE user SET profile_picture=%s WHERE email=%s"
        cursor.execute(sql, (pic_url, email))
        db_conn.conn.commit()
        print("Content-type:text/html")
        print()
        # print(code)
        print(image)
    else:
        print("Content-type:text/html")
        print()
        # print(code)

