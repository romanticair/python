"""
套接字用于夸任务通信：启动线程，相互通过套接字通信；也使用与独立程序，
因为套接字是系统级别的，类似FIFO；某些套接字服务器可能还需要与线程或
进程中的客户端通信；套接字传输字节字符串，后者可以是Pickle后的对象或
编码后的Unicode文本；
注意：如果线程打印输出重叠的话，仍需要同步化操作
"""

from socket import socket, AF_INET, SOCK_STREAM

port = 50008                               # 机器上套接字的端口号标识符
host = 'localhost'                         # 在这里服务器和客户端在同一台本地机器上运行


def server():
    sock = socket(AF_INET, SOCK_STREAM)    # tcp连接的ip地址
    sock.bind(('', port))                  # 绑定到这台机器的端口上
    sock.listen(5)                         # 允许最多5个等待中的客户端
    while True:
        conn, addr = sock.accept()         # 等待客户端连接#
        data = conn.recv(1024)             # 从这个客户端读取字节数据
        reply = 'server got: [%s]' % data  # conn是一个新连接上的套接字
        conn.send(reply.encode())          # 将字节化的回复发回客户端


def client(name):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))             # 连接到一个套接字端口
    sock.send(name.encode())               # 向监听者发送字节数据
    reply = sock.recv(1024)                # 从监听者那里接受字节数据
    sock.close()                           # 消息最多包含1024字节
    print('client got: [%s]' % reply)


if __name__ == '__main__':
    from threading import Thread
    sthread = Thread(target=server)
    sthread.daemon = True                 # 不等待服务器线程
    sthread.start()                        # 等待子线程结束
    for i in range(5):
        Thread(target=client, args=('client%s' % i,)).start()
