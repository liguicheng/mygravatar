#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import base64
import cgi, cgitb
import hashlib

import web
import mysql.connector


def changePic(base64URL, email):
    pic_type = base64URL.split(';')[0].split('/')[1]
    code = base64URL.split(',')[1]

    pic_data = base64.b64decode(code)

    email_encode = hashlib.md5(email.encode(encoding='UTF-8')).hexdigest()
    pic_url = "pictures/" + email_encode + '.' + pic_type
    pic = open(pic_url, "wb")
    pic.write(pic_data)
    pic.close()

    # 把图片路径存到数据库
    return pic_url



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


# 获取数据
image  = form.getvalue('image')
email  = form.getvalue('email')



# changeUserPic更改头像
pic_url = changePic(image, email)
sql = "UPDATE user SET profile_picture = '" + pic_url + "' WHERE email = \'" + email + "\'";
cursor.execute(sql)
db.commit()



# getUserPic根据邮箱获取头像
# email = '1098668564@qq.com'
# sql = "select profile_picture from user where email=\'" + email + "\'"
# cursor.execute(sql)
# pic_url =  [x[0] for x in cursor.fetchall()][0]
# code = getUserPic(pic_url)


print("Content-type:text/html")
print()
# print(code)
print(image)



# print("<html>")
# print("<head>")
# # print("<meta charset=\"utf-8\">")
# print("<title>Profile</title>")
# print("</head>")
# print("<body>")
#
# print("</body>")
# print("</html>")