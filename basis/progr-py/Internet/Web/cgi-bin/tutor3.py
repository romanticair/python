#!usr/bin/python
"""
在服务器上运行，读取表单输入，打印HTML，
url=http://server-name/cgi-bin/tutor3.py
"""
import cgi

form = cgi.FieldStorage()   # 解析表单数据
print("Content-type: text/html")

html = """
<title>tutor3.py</title>
<h1>Greetings</h1>
<hr>
<p>%s</p>
<hr>"""

if not "user" in form:
    print(html % "Whon are you?")
else:
    print(html % ("Hello, %s" % (form["user"].value)))
