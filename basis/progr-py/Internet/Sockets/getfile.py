"""
###########################################################################################
实现客户端和服务器逻辑，通过套接字从服务器传输任意文件到客户端；使用一个简单的控制信息
协议，而不是单独的套接字，用于控制和数据（如在FTP上），分派每个客户端请求到一个处理线程，
通过分块，循环传输整个文件；
###########################################################################################
"""

import os
import sys
import time
import _thread as thread
from socket import *

blksz = 1024
defaultHost = 'localhost'
defaultPort = 50001

helptext = """
Usage...
server=> getfile.py -mode server             [-port nnn] [-host hhh|localhost]
client=> getfile.py [-mode client] -file fff [-port nnn] [-host hhh|localhost]
"""


def now():
    return time.asctime()


def parsecommandline():
    dict = {}
    args = sys.argv[1:]            # put in dictionary for easy lookup
    while len(args) >= 2:         # skip program name at front of args
        dict[args[0]] = args[1]    # example: dict['-mode'] = 'server'
        args = [args[2:]]
    return dict


def client(host, port, filename):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.send((filename + '\n').encode())      # send remote name with dir: bytes
    dropdir = os.path.split(filename)[1]         # filename at end of dir path
    file = open(dropdir, 'wb')                   # create local file in cwd
    while True:
        data = sock.recv(blksz)                  # get up to 1K at a time
        if not data:                            # till closed on server side
            break                               # store data in local file
        file.write(data)
    sock.close()
    file.close()
    print('Client got', filename, 'at', now())


def serverthread(clientsock):
    sockfile = clientsock.makefile('r')       # wrap socket in dup file obj
    filename = sockfile.readline()[:-1]       # get filename up to end-line
    try:
        file = open(filename, 'rb')
        while True:
            bytes = file.read(blksz)          # read/send 1K at a time
            if not bytes:                    # until file totally sent
                break
            sent = clientsock.send(bytes)
            assert sent == len(bytes)
    except:
        print('Error downloading file on server:', filename)
    clientsock.close()


def server(host, port):
    serversock = socket(AF_INET, SOCK_STREAM)  # listen on TCP/TP socket
    serversock.bind((host, port))              # serve clients in threads
    serversock.listen(5)
    while True:
        clientsock, clientaddr = serversock.accept()
        print('Server connected by', clientaddr, 'at', now())
        thread.start_new_thread(serverthread, (clientsock,))


def main(args):
    host = args.get('-host', defaultHost)          # use args or defaults
    port = int(args.get('-port', defaultPort))     # is a string in argv
    if args.get('-mode') == 'server':              # None if no -mode: client
        if host == 'localhost':
            host = ''                              # else fails remotely
        server(host, port)
    elif args.get('-file'):                        # client mode needs -file
        client(host, port, args['-file'])
    else:
        print(helptext)

if __name__ == '__main__':
    args = parsecommandline()
    main(args)
