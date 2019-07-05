"""
####################################################################################
# 测试socket_stream redirection.py 模式
####################################################################################
"""
import os
import sys
import multiprocessing
from socket_stream_redirect import *

####################################################################################
# redirected client output
####################################################################################


def server1():
    mypid = os.getpid()
    conn = init_listener_socket()                    # block till client connect
    file = conn.makefile('r')
    for i in range(3):                              # read/recv client's prints
        data = file.readline().rstrip()              # block till data ready
        print('server %s got [%s]' % (mypid, data))  # print normally to terminal


def client1():
    mypid = os.getpid()
    redirect_out()
    for i in range(3):
        print('client %s:%s' % (mypid, i))           # print to socket
        sys.stdout.flush()                           # else buffered till exits!

####################################################################################
# redirected client input
####################################################################################


def server2():
    mypid = os.getpid()
    conn = init_listener_socket()                    # raw socket not buffered
    for i in range(3):                              # send client's prints
        conn.send(('server %s: %s\n' % (mypid, i)).encode())


def client2():
    mypid = os.getpid()
    rediret_in()
    for i in range(3):
        data = input()                               # input from socket
        print('client %s got [%s]' % (mypid, data))  # print normally to terminal

####################################################################################
# redirected client input + output, client is socket client
####################################################################################


def server3():
    mypid = os.getpid()
    conn = init_listener_socket()                  # wait for client connect
    file = conn.makefile('r')                      # recv print(), send input()
    for i in range(3):                            # readline blocks till data
        data = file.readline().rstrip()
        conn.send(('server %s got[%s]\n' % (mypid, data)).encode())


def client3():
    mypid = os.getpid()
    redirect_both_as_client()
    for i in range(3):
        print('client %s: %s' % (mypid, i))                       # print to socket
        data = input()                                            # input from socket: flushed!
        sys.stderr.write('client %s got [%s]\n' % (mypid, data))  # not redirected

####################################################################################
# redirected client input + output, client is socket server
####################################################################################


def server4():
    mypid = os.getpid()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    file = sock.makefile('r')
    for i in range(3):
        sock.send(('server %s: %s\n' % (mypid, i)).encode())      # send to input()
        data = file.readline().rstrip()                           # recv from print()
        print('server %s got [%s]' % (mypid, data))               # result to terminal


def client4():
    mypid = os.getpid()
    redirect_both_as_server()                          # I'm actually the socket server in this mode
    for i in range(3):
        data = input()                                 # input from socket: flushed!
        print('client %s got [%s]' % (mypid, data))    # print to socket
        sys.stdout.flush()                             # else last buffered till exit!

####################################################################################
# redirected client input + output, client is socket client, server xfers first
####################################################################################


def server5():
    mypid = os.getpid()                              # test 4, but server accepts
    conn = init_listener_socket()                    # wait for client connect
    file = conn.makefile('r')                        # send input(). recv print()
    for i in range(3):
        conn.send(('server %s: %s\n' % (mypid, i)).encode())
        data = file.readline().rstrip()
        print('server %s got [%s]' % (mypid, data))


def client5():
    mypid = os.getpid()
    s = redirect_both_as_client()                      # I'm the socket client in this mode
    for i in range(3):
        data = input()                                 # input from socket: flushes!
        print('client %s got [%s]' % (mypid, data))    # print to socket
        sys.stdout.flush()                             # eles last buffered till exit!

####################################################################################
# test by number on command-line
####################################################################################

if __name__ == '__main__':
    server = eval('server' + sys.argv[1])
    client = eval('client' + sys.argv[1])            # client in this process
    multiprocessing.Process(target=server).start()   # server in new process
    client()                                         # reset streams in client
    # import time;time.sleep(5)                      # test effect of exit flush
