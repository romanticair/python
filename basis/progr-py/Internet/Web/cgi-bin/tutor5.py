#!usr/bin/python
"""
在服务器上运行，读取表单输入，打印HTML
"""
import cgi
import sys

form = cgi.FieldStorage()
print('Content-type: text/html')

html = """
<title>tutor5.py</title>
<h1>Greeting</h1>
<hr>
<h4>Your name is %(name)s</h4>
<h4>You wear rather %(shoesize)s shoes</h4>
<h4>You current job: %(job)s</h4>
<h4>You program in %(language)s</h4>
<h4>You alse said:</h4>
<p>%(comment)s</p>
"""
data = {}
for field in ("name", "shoesize", "job", "language", "comment"):
    if not field in form:
        data[field] = "(unkonw)"
    else:
        if not isinstance(form[field], list):
            data[field] = form[field].value
        else:
            values = [x.value for x in form[field]]
            data[field] = " and ".join(values)

print(html % data)
