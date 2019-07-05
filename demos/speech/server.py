"""
speech 的服务器，用于用户聊天通信
"""
import time
import socket
import threading

SOCK_LIST = []


def tcplink(sock, addr):
    SOCK_LIST.append(sock)
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024).decode('utf-8')
        time.sleep(1)
        if data == 'exit':
            break

        # 转发数据
        print('%s %s' % (addr, data))
        while len(SOCK_LIST) < 2:
            time.sleep(1)

        for s in SOCK_LIST:
            if s is not sock:
                s.send(data.encode('utf-8'))
                break

    SOCK_LIST.remove(sock)
    sock.close()
    print('Connection from %s:%s closed.' % addr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9000))
server.listen(3)
print('Server started\nWaiting for connection...')

while True:
    sock, addr = server.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
