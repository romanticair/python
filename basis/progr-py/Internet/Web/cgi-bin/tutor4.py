#!usr/bin/python
"""
在服务器上运行，读取表单输入，打印HTML
url http://server-name/cgi-bin/tutor4.py
"""

import cgi
import sys

sys.stderr = sys.stdout      # 将错误传给浏览器
form = cgi.FieldStorage()    # 解析表单
print("Content-type: text/html\n")

html = """
<title>tutor4.py</title>
<h1>Greeting</h>
<hr>
<h4>%s</h4>
<h4>%s</h4>
<h4>%s</h4>
<hr>
"""
if "user" not in form:
    line1 = "who are you?"
else:
    line1 = "Hello, %s" % form["user"].value

line2 = "Your're talking to a %s server." % sys.platform
line3 = ""
if "age" in form:
    try:
        line3 = "Your age squared is %d!" % int(form["age"].value) ** 2
    except:
        line3 = "Sorry, I can't compute %s ** 2." % form["age"].value

print(html % (line1, line2, line3))