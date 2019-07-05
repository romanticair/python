"""
与fork_server.py一样，但是使用Python的signal模块来避免保持子僵尸进程在终止后还逗
留，而不是在每个新连接前，使用显示的捕获捕获循环；SIG_IGN表示忽略，可能并不使用于
所有平台上的SIG_CHLD子进程退出信号；参考Linux文档，了解更多有关socket.accept调用
因信号中断而重启的内容；
"""
import os
import sys
import time
import signal
from socket import *

myHost = ''                                    # '' = all available interfaces on host
myPort = 50007                                 # listen on non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)         # make a TCP socket object
sockobj.bind((myHost, myPort))                 # bind it to server port number
sockobj.listen(5)                              # listen, allow 5 pending connects
signal.signal(signal.SIGCHLD, signal.SIG_IGN)  # avoid child zombie processed


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
    os._exit(0)


def dispatcher():                                     # listen until process killed
    while True:                                        # wait for next connection,
        connection, address = sockobj.accept()          # pass to precess for service
        print('Server connected by', address, end='')
        print('at', now())
        childPid = os.fork()                            # copy this process
        if childPid == 0:                               # if in child process: handle
            handle_client(connection)                   # else: go accept next connect

dispatcher()
