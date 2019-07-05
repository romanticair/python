import os
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = '.'   # HTML文件和cgi脚本目录所在处
port = 80      # 80 -> http://servername/, other -> http://servername:xxx/

if len(sys.argv) > 1:
    webdir = sys.argv[1]
if len(sys.argv) > 2:
    port = int(sys.argv[2])

print('webdir "%s", port %s' % (webdir, port))

os.chdir(webdir)                  # 在HTML根目录下运行
serveraddr = ('', port)           # 托管服务器名称，端口号
serverobj = HTTPServer(serveraddr, CGIHTTPRequestHandler)
serverobj.serve_forever()         # 服务于客户端，直到退出
