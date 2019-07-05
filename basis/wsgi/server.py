from wsgiref.simple_server import make_server
from hello import *  # 导入 application 函数

# 创建一个服务器，IP地址为空，端口 8000，处理函数是 application2
httpd = make_server('', 8000, application2)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求
httpd.serve_forever()
