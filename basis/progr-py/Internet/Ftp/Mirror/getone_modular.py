"""
一个通过FTP下载并播放媒体文件的Python脚本，使用getfile.py，一个封装了FTP步骤
的工具模块
"""
import getfile
from getpass import getpass

filename = 'monkeys.jpg'             # 远程/本地文件名

# 用工具模块抓取
getfile.getfile(file=filename, site='ftp.rmi.net', dir='.',
                user=('lutz', getpass('Pswd?')), refetch=True)

if input('Open file?') in ['y', 'Y']:
    from Tools.playfile import playfile
    playfile(filename)
