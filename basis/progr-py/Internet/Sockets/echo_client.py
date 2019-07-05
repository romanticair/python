"""
客户端：使用套接字来发送数据到服务器，输出服务器答复到每条信息行；'localhost'意味着，
服务器和客户端是运行在同一台机器上的，可以让我们在同一台机器上测试客户端和服务器；为
了测试互联网，在远程机器上运行服务器，并设置server Host或argv[1]到机器域名或IP地址；
Python的套接字是一个可移植的BSD套接字接口，在系统C库中可获得标准套接字调用的对象方法。
"""

import sys
from socket import *                          # portable socket interface plus constants

serverHost = 'localhost'                        # server name, or: 'starship.python.net'
serverPort = 50007                              # non-reserved port used by the server

message = [b'Hello network world']              # default text to send to server
                                                # requires bytes: b'' or str.encode()
if len(sys.argv) > 1:
    serverHost = sys.argv[1]                    # server from cmd line arg 1
if len(sys.argv) > 2:                           # text from cmd line args 2..n
    message = (x.encode() for x in sys.argv[2:])

                                                 # AF_INTET mean the IP, SOCK_STEAM mean the TCP
sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP/IP socket object
sockobj.connect((serverHost, serverPort))         # connect to server machine + port

for line in message:
    sockobj.send(line)                     # send line to server over socket
    data = sockobj.recv(1024)              # receive line from server: uo to 1k
    print('Client received:', data)        # bytes are quoted, was 'x', repy(x)

sockobj.close()                            # close socket to send eof to server
