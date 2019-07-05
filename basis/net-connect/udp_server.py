# 相对TCP，UDP则是面向无连接的协议
# 使用UDP协议时，不需要建立连接，只需要知道对方的IP地址和端口号，就可以直接发数据包
import socket

# 服务端
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))
# SOCK_DGRAM指定了这个Socket的类型是UDP。绑定端口和TCP一样，但是不需要调用listen()方法
# 直接接收来自任何客户端的数据
print('Bind UPD on 9999...')
while True:
    # 接收数据
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)
