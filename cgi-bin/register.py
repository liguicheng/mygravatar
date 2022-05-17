#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi
import hashlib
import string
import random
import MySQL
import threading


def check_available():
    pass


def check_user_exist(email):
    cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
    result = cursor.fetchall()  # fetchall() 获取所有记录
    if len(result) != 0:
        return True
    else:
        return False


def insert(name, email, picture, password):
    # 判断用户是否存在，防止并发问题
    with lock:
        flag = check_user_exist(email)
        if not flag:
            # 头像要先弄一个默认的，插入user表
            sql_user = "INSERT INTO user (username, email, profile_picture) VALUES (%s, %s, %s)"
            val_user = [(name, email, picture)]
            cursor.executemany(sql_user, val_user)

            user_id_sql = "SELECT id FROM user WHERE email=%s"
            cursor.execute(user_id_sql, (email,))
            user_id = [x[0] for x in cursor.fetchall()][0]

            # 对密码进行加密，插入密码表
            # 1. 准备一个字符集用于生成随机字符串，字符集只包含字母和数字
            charset = string.ascii_letters + string.digits
            # 2. 生成一个随机字符串作为盐，长度为32
            salt = ''.join(random.sample(charset, 32))
            # 3. 将盐和密码拼在一起算哈希值
            salted_hash = hashlib.sha256((salt + password).encode(encoding='UTF-8')).hexdigest()
            # 4. 将盐和哈希值拼在一起保存到数据库
            salt_password = '{}-{}'.format(salt, salted_hash)
            sql_password = "INSERT INTO user_password (password, user_id) VALUES (%s, %s)"
            val_password = [(salt_password, user_id)]
            cursor.executemany(sql_password, val_password)
            db_conn.conn.commit()
            return True
        else:
            return False


db_conn = MySQL.MySQLConn()
cursor = db_conn.get_cursor()

lock = threading.Lock()

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage()

# 获取数据
name = form.getvalue('name')
email  = form.getvalue('email')
password  = form.getvalue('password')
# 需要使用默认的头像
picture = "pictures/default.png"

print("Content-type:text/html")
print()
print(insert(name, email, picture, password))


