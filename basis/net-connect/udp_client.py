"""
UDP的使用与TCP类似，但是不需要建立连接。此外，服务器绑定
UDP端口和TCP端口互不冲突，也就是说，UDP的9999端口与TCP的
9999端口可以各自绑定
"""
import socket

# 客户端
# 不需要调用 connect()，直接通过 sendto() 给服务器发数据
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据
    print(s.recv(1024).decode('utf-8'))

s.close()
