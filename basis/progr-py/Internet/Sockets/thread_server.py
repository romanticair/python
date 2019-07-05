"""
服务器端：在端口上打开一个套接字，监听来自客户端的消息，发送一个相应答复；相应行一直到
EOF，当客户端关闭套接字的时候；派生一个线程来处理每个客户端里阿尼额；线程与主线程共享
全局内存空间；这比分支更具有可移植性：线程可以运行在标准Windows系统上，但是进程分支不行。
"""
import time
import _thread as thread
from socket import *

myHost = ''                                    # '' = all available interfaces on host
myPort = 50007                                 # listen on non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)         # make a TCP socket object
sockobj.bind((myHost, myPort))                 # bind it to server port number
sockobj.listen(5)                              # listen, allow 5 pending connects


def now():
    return time.ctime(time.time())            # current time on server


def handle_client(connection):                 # child process: reply, exit
    time.sleep(5)                                 # simulate a blocking activity
    while True:                                 # read, write a client socket
        data = connection.recv(1024)              # till eof when socket closed
        if not data:
            break
        reply = 'Echo=>%s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()


def dispatcher():                                     # listen until process killed
    while True:                                        # wait for next connection,
        connection, address = sockobj.accept()          # pass to thread for service
        print('Server connected by', address, end='')
        print('at', now())
        thread.start_new_thread(handle_client, (connection,))

dispatcher()
