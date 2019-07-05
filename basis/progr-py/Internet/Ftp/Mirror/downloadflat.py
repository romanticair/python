"""
#################################################################################################
使用FTP将远程站点的单个目录下所有文件复制（下载）到本地及其上的目录；定期运行，在你的ISP账号
里制作扁平型FTP站点目录的镜像；如果想镜像匿名FTP操作，把用户设置为 'anonymous'；我们也可以尝试
在每次传输之前用一个新的FTP实例来重新进行连接：只连接一次；如果发生失败，对于主动FTP可以试试
把设置改为非被动，或者禁用防火墙；这一点也取决于工作的FTP服务器，可能在于其加载策略。
#################################################################################################
"""
import os
import sys
import ftplib
from getpass import getpass
from mimetypes import guess_type

nonpassive = False                    # 默认为被动FTP
remotesite = 'home.rmi.net'            # 从这个站点下载
remotedir = '.'                        # 这个目录(如public_html)
remoteuser = 'lutz'
remotepass = getpass('Password for %s on %s: ' % (remoteuser, remotesite))
localdir = (len(sys.argv) > 3 and sys.argv[1]) or '.'
cleanall = input('Clean local directory first? ')[:1] in ['y', 'Y']
print('connecting...')
connection = ftplib.FTP(remotesite)         # 连接到FTP站点
connection.login(remoteuser, remotepass)    # 用户名/密码登录
connection.cwd(remotedir)                   # 进入待复制目录
if nonpassive:                              # 强制主动FTP模式
    connection.set_pasv(False)             # 多数服务器采用被动模式
if cleanall:
    for localname in os.listdir(localdir):  # 尝试删除所有本地文本
        try:
            print('deleting local', localname)
            os.remove(os.path.join(localdir, localname))
        except:
            print('cannot delete local', localname)

count = 0                                     # 下载所有远程文件
remotefiles = connection.nlst()               # nlst()给出文件列表
for remotename in remotefiles:
    if remotename in ('.', '..'):
        continue                                # 某些服务器包括.和..目录
    mimetype, encoding = guess_type(remotename)  # 比如('text/plain', 'gzip')
    mimetype = mimetype or '?/?'                 # 可以是(None, None)
    maintype = mimetype.split('/')[0]            # 对于.jpg文件: ('image/jpeg', None)
    localpath = os.path.join(localdir, remotename)
    print('downloading', remotename, 'to', localpath, end='')
    print('as', maintype, encoding or '')
    if maintype == 'text' and encoding is None:
        # 以ascii模式和文本文件进行传输
        # 使用和ftplib兼容的编码体系
        localfile = open(localpath, 'w', encoding=connection.encoding)
        callback = lambda line: localfile.write(line + '\n')
        connection.retrlines('RETR ' + remotename, callback)
    else:
        # 以二进制模式和字节文件进行传输
        localfile = open(localpath, 'wb')
        connection.retrbinary('RETR ' + remotename, localfile.write)
    localfile.close()
    count += 1

connection.quit()
print('Done:', count, 'files downloaded.')
