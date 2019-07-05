#!usr/bin/python
"""
一个通过URL字符串从FTP下载文件的Python脚本；抓取文件时使用高级的urllib代替ftplib；
urllib支持FTP、HTTP、客户端HTTP和本地文件，并控制代理、重定向、cookies等；urllib
还允许下载html页面、图像、文本等；惯有urllib抓取来的网页可参看 Python html/xml解析器
"""
import os
import getpass
from urllib.request import urlopen                  # 基于套接字的网络工具

filename = 'monkeys.jpg'             # 远程/本地文件名
password = getpass.getpass('Pswd?')  # 需要命令行模式才有输入

remoteaddr = 'ftp://lutz:%s@ftp.rmi.net/%s;type=i' % (password, filename)
print('Downloading', remoteaddr)

# 也可以这样:
# urllib.request.urlretrieve(remoteaddr, filename)

remotefile = urlopen(remoteaddr)     # 返回类文件输入对象(一个基于FTP的套接字流)
localfile = open(filename, 'wb')     # 本地存储数据的位置
localfile.write(remotefile.read())
localfile.close()
remotefile.close()
