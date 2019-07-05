"""
同样的套接字，除了在线程间通信，还在独立程序间通信；此处的
服务器在进程中运行，为线程和进程中的客户端提供服务；套接字
是机器水平的全局对象，类似fifo，无须共享内存
"""
import os
import sys
from threading import Thread
from socket_preview import server, client


mode = int(sys.argv[1])
if mode == 1:                                   # 此进程中运行服务器
    server()
elif mode == 2:                                 # 此进程中运行客户端
    client('client: process=%s' % os.getpid())
else:                                           # 在进程中运行5个客户端线程
    for i in range(5):
        Thread(target=client, args=('client:thread=%s' % i,)).start()