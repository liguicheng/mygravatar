#!C:\ProgramData\Anaconda3\python.exe
# -*- coding: UTF-8 -*-

# CGI处理模块
import os
import http.cookies


cookie = http.cookies.SimpleCookie(os.environ.get('HTTP_COOKIE'))
cookie['token'] = "clear"
cookie['token']['path'] = "/"

print("Content-type:text/html")
print(cookie)
print()
