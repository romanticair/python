"""
借助Urllib,从HTTP(网络)服务器经由套接字抓取文件；这个版本使用的接口将所抓取的数据
保存到一个本地二进制模式文件中；本地文件名作为命令行参数传入或者用urllib.parse从URL
提取而来：文件名参数可能都一样目录路径，末尾带有查询参数，所以用os.path.split处理还
不够(仅仅割了目录路径)；
缺陷：应该用urllib.parse.quote处理文件名，除非已经知道文件名没问题；
"""
import os
import sys
import urllib.request
import urllib.parse

showline = 6
try:
    servername, filename = sys.argv[1:3]
except:
    servername, filename = 'learning-python.com', '/index.html'

remoteaddr = 'http://%s%s' % (servername, filename)   # 任何网络地址
if len(sys.argv) == 4:                                # 获取结果文件名
    localname = sys.argv[3]
else:
    (scheme, server, path, parms, query, frag) = urllib.parse.urlparse(remoteaddr)
    localname = os.path.split(path)[1]

print(remoteaddr, localname)
urllib.request.urlretrieve(remoteaddr, localname)     # 可以是文本或脚本
remotedata = open(localname, 'rb').readlines()        # 保存到本地文件
for line in remotedata[:showline]:                   # 文件是字节/二进制
    print(line)
