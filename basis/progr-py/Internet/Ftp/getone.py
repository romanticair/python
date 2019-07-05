#!usr/bin/python
"""
一个借助FTP下载并播放媒体文件的Python脚本。使用ftplib，用套接字的ftp协议处理器。FTP在
两个套接字上运行（一个用于数据，一个用于控制 ---- 分别使用端口20和21）并且规定消息文本
格式，但Python的ftplib模块隐藏了该协议的大部分细节，根据你的站点/文件作出修改。
"""

import os
import sys
from ftplib import FTP                              # 基于套接字发FTP工具
from getpass import getpass                         # 隐藏密码输入

nonpassive = False                                   # 是否强制服务器进入主动FTP模式?
filename = 'monkeys.jpg'                              # 将要下载的文件
dirname = '.'                                         # 将要抓取的远程目录
sitename = 'ftp.rmi.net'                              # 将要连接的FTP站点
# passwd = getpass('Pswd?')
# userinfo = ('lutz', passwd)
userinfo = ('lutz', getpass('Pswd?'))                 # 匿名登录则使用()
if len(sys.argv) > 1:                                 # 文件名是否包含在命令行中
    filename = sys.argv[1]

print('Connecting....')
connection = FTP(sitename)                # 连接到FTP站点
connection.login(*userinfo)               # 默认为匿名登录
connection.cwd(dirname)                   # 每次将1K数据传送到本地文件
if nonpassive:                            # 如果服务器要求则强制主动FTP模式
    connection.set_pasv(False)

print('Downloading...')
localfile = open(filename, 'wb')          # 用于存储下载内容的本地文件
connection.retrbinary('RETR ' + filename, localfile.write, 1024)
connection.quit()                         # 'FETR 文件名' 是FTP抓取的标准格式
localfile.close()

if input('Open file?') in ['y', 'Y']:
    from Tools.playfile import playfile
    playfile(filename)
