# WSGI：Web Server Gateway Interface。

# 这里实现 Web 应用程序的 WSGI 处理函数
# 再编写一个负责启动 WSGI 服务器，加载 application 函数的服务器
# 用 Web 开发者实现一个函数，就可以响应 HTTP 请求


def application1(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']


def application2(environ, start_Response):
    start_Response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]

# application() 函数是符合 WSGI 标准的一个 HTTP 处理函数，它接收两个参数
# environ：一个包含所有HTTP请求信息的dict对象
# start_response：一个发送HTTP响应的函数
# Header 只能发送一次

# start_response() 函数接收两个参数
# 一个是 HTTP 响应码，一个是一组 list 表示的 HTTP Header
# 每个 Header 用一个包含两个 str 的 tuple 表示

# 运行 WSGI 服务
# > server.py
