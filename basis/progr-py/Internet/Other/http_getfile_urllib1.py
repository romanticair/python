"""
借助urllib, 从HTTP(网络)服务器经由套接字抓取文件；urllib通过URL地址字符串支持HTTP、
FTP、文件及HTTPS；对于HTTP，这个URL可以指定文件或触发远程CGI脚本；通过网络抓取文件在
Python中可以用多种不同方式实现，其代码对服务器的要求各有不同：通过套接字、FTP、HTTP
urllib和CGI输出，缺陷：应当通过urllib.parse.quote运行文件名以便正确进行转义，除非文件名
被硬编码指定；
"""
import sys
from urllib.request import urlopen

showline = 6
try:
    servername, filename = sys.argv[1:]
except:
    servername, filename = 'learning-python.com', '/index.html'

remotedir = 'http://%s%s' % (servername, filename)  # 也可以指定一个CGI脚本
print(remotedir)
remotefile = urlopen(remotedir)                     # 返回输入文件对象
remotedata = remotefile.readlines()                 # 此处直接读取数据
remotefile.close()

for line in remotedata[:showline]:
    print(line)                                     # 嵌有\n的字节
