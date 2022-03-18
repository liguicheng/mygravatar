#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import cgi, cgitb
import os

import mysql.connector
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
# cookie['email']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
cookie['email'] = "clear"

print("Content-type:text/html")
print(cookie)
print()
