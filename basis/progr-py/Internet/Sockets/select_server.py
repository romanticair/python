"""
服务器：使用select并行处理多个客户端，使用select模块手动在套接字之间多重通道传输：
接收新的客户端连接的主套接字，并输入套接字链接到接收的客户端；select可以采用可选的
第四个参数0来轮询，用n.m等待n.m秒，或者忽略直接等待直到任意套接字准备好了，再处理。
"""

import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

numPortSocks = 2                               # number of ports for client connects
myHost = ''                                    # '' = all available interfaces on host
myPort = 50007                                 # listen on non-reserved port number
if len(sys.argv) == 3:
    myHost, myPort = sys.argv[1:]


def now():
    return time.ctime(time.time())

# make main sockets for accepting new client requests
mainsocks, readsocks, writesocks = [], [], []
for i in range(numPortSocks):
    portsock = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
    portsock.bind((myHost, myPort))              # bind it to server port number
    portsock.listen(5)                           # listen, allow 5 pending connects
    mainsocks.append(portsock)                   # add to main list to identify
    readsocks.append(portsock)                   # add to select inputs list
    myPort += 1                                  # bind on consecutive ports

# event loop: listen and multiplex until server process killed
print('select-server loop starting')
while True:
    # print(readsocks)
    readables, writeables, exceptions = select(readsocks, writesocks, [])
    for sockobj in readables:
        if sockobj in mainsocks:                          # for ready input sockets
            # port socket: accept new client
            newsock, address = sockobj.accept()            # accept should not block
            print('connect:', address, id(newsock))        # newsock is a new socket
            readsocks.append(newsock)                      # add to select list, wait
        else:
            # client socket: read next line
            data = sockobj.recv(1024)                      # recv should not block
            print('\tgot', data, 'on', id(sockobj))
            if not data:                                  # if closed by the clients
                sockobj.close()                            # close here and remv from
                readsocks.remove(sockobj)                  # del list else reselected
            else:
                # this may block: should readlly select for writes too
                reply = 'Echo=>%s at %s' % (data, now())
                sockobj.send(reply.encode())
