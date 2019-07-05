"""
服务器端：在某一端口上开启一个TCP/IP套接字，监听来自客户端的消息，并且发送一个应答；
这是一个简单的每个客户端一次的listen/reply会话，但它进入一个无限循环来监听更多的客
户端，只要这个服务器脚本一直运行，客户端可能运行在远程机器上，或者如果使用"本地主机"
作为服务器，那么就在同一台计算机上运行。
"""
from socket import *                       # get socket constructor and constants

myHost = ''                                  # '' = all available interfaces on host
myPort = 50007                               # listen on non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)       # make a TCP socket object
sockobj.bind((myHost, myPort))               # bind it to server port number
sockobj.listen(5)                            # listen, allow 5 pending connects

while True:                                 # listen until process killed
    connection, address = sockobj.accept()   # wait for next client connect
    print('Server connected by', address)    # connection is a new socket
    while True:
        data = connection.recv(1024)         # read next line on client socket
        if not data:
            break                           # send a reply line to the client
        connection.send(b'Echo=>' + data)    # until eof when socket closed
    connection.close()
