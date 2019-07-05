"""
用法：sousa.py 抓取和播放Monty Python主题曲，不加修改的话，在你的系统上不能工作：它
需要一个台接入互联网的计算机和一个你可以访问的FTP服务器账户，使用Unix的音频滤波器，
在Windows上使用.au播放器。请针对你的平台，对这个脚本和playfile.py进行必要的配置。
"""

from getpass import getpass
from Internet.Ftp.getfile import getfile
from Tools.playfile import playfile

file = 'sousa.au'       # 默认文件参数
site = 'ftp.rmi.net'    # Monty Python主题曲
dir = '.'
user = ('lutz', getpass('Pswd?'))

getfile(file, site, dir, user)  # 通过FTP抓取音频文件
playfile(file)                  # 将其发送到音频播放器

# import os
# os.system('getone.py sousa.au')  # 等效的命令行
