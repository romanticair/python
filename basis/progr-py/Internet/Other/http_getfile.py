"""
借助http.client，从一台HTTP(网络)服务器上通过套接字抓取文本；文本名参数可以是
一个完整的目录路径，也可以通过末尾的?查询参数制定一个CGI脚本，触发一个远程程序；
抓取得到文件数据或远程程序输出可以保存到本地文件，以便模拟FTP功能，或者用str.find
或html.parser模块解析；另外，http.client.request(method, url, body=None, hdrs={});
"""
import sys
import http.client

showlines = 6

try:
    servername, filename = sys.argv[1:]
except:
    servername, filename = 'learning-python.com', '/index.html'

print(servername, filename)
server = http.client.HTTPConnection(servername)    # 连接到http站点/服务器
server.putrequest('GET', filename)                 # 发送请求和题头
server.putheader('Accept', 'text/html')            # 也可以用POST请求
server.endheaders()                                # CGI脚本文件名也可以

reply = server.getresponse()            # 读取回复的题头和数据
if reply.status != 200:                 # 200表示成功
    print('Error sending request', reply.status, reply.reason)
else:
    data = reply.readlines()            # 接收到的数据的文件对象
    reply.close()                       # 显示各行，末尾为换行符
    for line in data[:showlines]:      # 为完成存储，将数据写入文件
        print(line)                     # 行已经有了\n，不过是字节
