#!/usr/bin/python
import cgi
import html

form = cgi.FieldStorage()           # 解析表单数据
print('Content-Type: text/html')
print()
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print('<title>Reply Page</title>')  # html相应页面
print('</head>')
print('<body>')
if 'user' not in form:
    print('<h1>Who are you?</h1>')
else:
    # html.escape 可以转义html语言的特殊字符
    print('<h1>Hello <i>%s</i>!</h1>' % html.escape(form.getvalue('user')))

print('</body>')
print('</html>')
# 在上一级目录下python -m http.server --cgi
# 端口号默认8000， 可在 --cgi后面指定端口号
# 在网页输入localhost:8000/cgi101.html即可收到响应
# 说明：（服务器和客服端一体）
