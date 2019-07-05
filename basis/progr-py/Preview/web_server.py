"""
用Python实现一个HTTP Web服务器，它知道如何运行服务器端CGI脚本；
从当前工作目录提供文件和脚本，Python脚本必须存储在 webdir/cig-bin或
webdir/htbin中；
"""
import os
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

web_dir = '.'  # 存放HTML文件和cgi-bin脚本文件夹的所在
port = 8888    # 缺省http://localhost/, 也可以用http://localhost:xxxx/

os.chdir(web_dir)           # 在HTML根目录中运行
server_add = ('localhost', port)     # 我的主机名和端口号 127.0.0.1
server_obj = HTTPServer(server_add, CGIHTTPRequestHandler)
server_obj.serve_forever()  # 以永久的守护进程运行

# 可绕过传统的输入页面
# http://localhost:8888/cgi-bin/cgi101.py?user=Sue+Smith
