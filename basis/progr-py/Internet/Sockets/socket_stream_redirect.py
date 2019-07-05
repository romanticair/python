"""
####################################################################################
用于连接非GUI程序的标准流的一个套接字的工具，一个GUI（或其它）程序可以使用
这与非GUI程序进行交互。
####################################################################################
"""
import sys
from socket import *

port = 50007
host = 'localhost'


def init_listener_socket(port=port):
    """
    初始化在服务器模式下调用者用于监听的连接套接字
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(5)
    conn, addr = sock.accept()
    return conn


def redirect_out(port=port, host=host):
    """
    在接收之前其它连接失败，连接调用者标准输出流到一个套接字，这个套接字用于GUI监听，
    在收听者启动后，启动调用者
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))                   # caller operates in clients mode
    file = sock.makefile('w')                    # file interface: text, buffered
    sys.stdout = file                            # make prints go to sock.send
    return sock                                 # if caller needs to accese it raw


def rediret_in(port=port, host=host):
    """
    连接调用者标准输入流到用于GUI来提供功能的套接字
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    file = sock.makefile('r')                    # file interface wrapper
    sys.stdin = file                             # make input come from sock.recv
    return sock                                 # return value can be ignored


def redirect_both_as_client(port=port, host=host):
    """
    在这种模式下，连接调用者标准输入和输出流到相同的套接字，调用者对于服务器
    来说就是客户端：发送消息，接收响应
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))             # or open in 'rw' mode
    ofile = sock.makefile('w')             # file interface: text, buffered
    ifile = sock.makefile('r')             # two file objects wrap same socket
    sys.stdout = ofile                     # make prints go to socket.send
    sys.stdin = ifile                      # make input come from sock.recv
    return sock


def redirect_both_as_server(port=port, host=host):
    """
    在这种模式下，连接调用者标准输入和输出流到相同的套接字，调用者对于客户端
    来说就是服务器：接收消息，发送响应答复
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))                # or open in 'rw' mode
    sock.listen(5)
    conn, addr = sock.accept()
    ofile = conn.makefile('w')             # file interface wrapper
    ifile = conn.makefile('r')             # two file objects wrap same socket
    sys.stdout = ofile                     # make prints go to socket.send
    sys.stdin = ifile                      # make input come from sock.recv
    return conn
