#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi
import hashlib
import MySQL
import datetime
import jwt
import time

def check_user_exist(email):
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
    result = cursor.fetchall()  # fetchall() 获取所有记录
    if len(result) != 0:
        return True
    else:
        return False


def check_password(email, password):
    # 需要把密码加密了，然后看与数据库中加密后的密码一样不
    user_id_sql = "SELECT id FROM user WHERE email=%s"
    cursor.execute(user_id_sql, (email,))
    # 获取从数据库中选出的数据
    user_id = [x[0] for x in cursor.fetchall()][0]

    sql_password = "SELECT password FROM user_password WHERE user_id=%s"
    cursor.execute(sql_password, (user_id,))

    # 从数据库取出密码，盐值，加盐哈希值分离，对登录的密码加盐哈希，判断密码是否相同
    salt_password = [x[0] for x in cursor.fetchall()][0]
    salt, salted_hash = salt_password.split('-')
    password_encode = hashlib.sha256((salt + password).encode(encoding='UTF-8')).hexdigest()

    if password_encode == salted_hash:
        return True
    else:
        return False


db_conn = MySQL.MySQLConn()
cursor = db_conn.get_cursor()

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取数据
email  = form.getvalue('email')
password  = form.getvalue('password')

# 身份过期时间为一天
expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=24*60*60), "%a, %d-%b-%Y %H:%M:%S GMT")

# 创建token
# 生成一个字典，包含我们的具体信息
d = {
    # 公共声明
    'exp': time.time() + 86400,  # (Expiration Time) 此token的过期时间的时间戳
    'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
    'iss': 'lgc',  # (Issuer) 指明此token的签发者

    # 私有声明
    'data': {
        'email': email,
        'timestamp': time.time()
    }
}

# pyjwt提供的jwt.encode(payload,key,algorithm)方法可以让我们快速的生成token；需要提供三个参数
# payload	 公有声明和私有声明组成的字典，根据需要进行添加
# key	     自定义的加密key。重要，不能外泄
# algorithm	 声明需要使用的加密算法，如’HS256’
token = jwt.encode(d, 'lgc12345', algorithm='HS256')


print("Content-type:text/html")
print("Set-Cookie: token=" + token + ";expires=" + expires + ";path=/")
print()
if not check_user_exist(email):
    print("NOT_EXIST")
else:
    print(check_password(email, password))
