# Socket是网络编程的一个抽象概念。通常我们用一个Socket表示“打开了一个网络链接”
# 而打开一个Socket需要知道目标计算机的IP地址和端口号，再指定协议类型即可

# 客户端(相对网页服务器)
# 创建一个基于TCP链接的Socket
import socket

# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接
s.connect(('www.sina.com.cn', 80)) # 端口80

# 发送数据
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# 接收数据
buffer = []
while True:
    # 每次最多接收1k字节
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break

data = b''.join(buffer)
# 关闭链接
s.close()
# 接收到的数据包括HTTP头和网页本身，我们只需要把HTTP头和网页分离一下，把HTTP头打印出来，网页内容保存到文件
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
with open('sina.html', 'wb') as f:
    f.write(html)
