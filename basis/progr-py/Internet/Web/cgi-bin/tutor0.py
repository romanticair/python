#!usr/bin/python
"""
在服务器上运行，打印HTML以生成新页面
url为 http://localhost/cgi-bin/tutor0.py
"""

# 题头和HTML代码必须有个空行隔开
print("Content-type: text/html\n")
print("<Title>CGI 101</Title>")
print("<h1>A First CGI Script</h1>")
print("<p>Hello, CGI World!</p>")
