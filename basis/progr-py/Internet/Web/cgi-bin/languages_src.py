#!/usr/bin/python
"不加运行而只是显示languages.py脚本的代码"

import html

filename = 'cgi-bin/languages.py'
print('Content-type: text/html\n')            # 封装在HTML中
print('<title>Languages</title>')
print('<h1>Source code: "%s"</h1>' % filename)
print('<hr><pre>')
print(html.escape(open(filename).read()))     # 遵照系统平台的默认设置进行解码
print('</pre><hr>')
