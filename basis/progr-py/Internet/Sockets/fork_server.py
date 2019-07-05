import sys
import time
from socket import *                       # get socket constructor and constants

myHost = ''                                  # '' = all available interfaces on host
myPort = 50007                               # listen on non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)       # make a TCP socket object
sockobj.bind((myHost, myPort))               # bind it to server port number
sockobj.listen(5)                            # listen, allow 5 pending connects


def now():
    return time.ctime(time.time())          # current time on server

activeChildren = []


def reap_children():                           # reap any dead child processed
    while activeChildren:                        # else may fill up system table
        pid, stat = os.waitpid(0, os.WNOHANG)     # don't hang if no child exited
        if not pid:
            break
        activeChildren.remove(pid)


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
        reap_children()                                 # clean up exited children now
        childPid = os.fork()                            # copy this process
        if childPid == 0:                               # if in child process: handle
            handle_client(connection)
        else:                                           # else: go accept next connect
            activeChildren.append(childPid)              # add to active child pid list

dispatcher()
