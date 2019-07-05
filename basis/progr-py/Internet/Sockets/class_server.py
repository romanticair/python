"""
服务器端：在端口打开一个套接字，监听来自客户端的消息，发送一个相应答复；这个类型使用
标准库模块的socketserver来完成运行；socketserver提供TCPServer，ThteadingTCPServer，
ForkingTCPServer，及其UDP的变体类型等，把每个客户端连接请求，路由到一个新传入的请求
处理器对象句柄方法的实例；socketserver还支持Unix域的套接字，但仅限于Unix；
"""
import time
import socketserver                           # get socket server, handler objects

myHost = ''                                    # '' = all available interfaces on host
myPort = 50007                                 # listen on non-reserved port number


def now():
    return time.ctime(time.time())


class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                                     # on each client connect
        print(self.client_address, now())                  # show this client's address
        time.sleep(5)                                      # simulate a blocking activity
        while True:                                       # self.request is client socket
            data = self.request.recv(1024)                 # read, write a client socket
            if not data:
                break
            reply = 'Echo=>%s at %s' % (data, now())
            self.request.send(reply.encode())
        self.request.close()

# make a threaded server, listen/handle clients forever
myaddr = (myHost, myPort)
server = socketserver.ThreadingTCPServer(myaddr, MyClientHandler)
server.serve_forever()
