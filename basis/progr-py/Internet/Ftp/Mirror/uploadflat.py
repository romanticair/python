"""
#################################################################################################
使用FTP从本地目录将所有文件上传到远程站点/目录，不如可以运行我，把你的网络/FTP站点文件，
从PC复制到你的ISP；假定扁平型目录上传：嵌套目录用uploadall.py，请参考downloadflat.py的
注释以获取更多说明：这两个脚本的操作时对称的。
#################################################################################################
"""
import os
import sys
import ftplib
from getpass import getpass
from mimetypes import guess_type

nonpassive = False                    # 默认为被动FTP
remotesite = 'learning-python.com'     # 上传到此站点
remotedir = 'books'                    # 这个目录(如public_html)
remoteuser = 'lutz'
remotepass = getpass('Password for %s on %s: ' % (remoteuser, remotesite))
localdir = (len(sys.argv) > 3 and sys.argv[1]) or '.'
cleanall = input('Clean remote directory first? ')[:1] in ['y', 'Y']
print('connecting...')
connection = ftplib.FTP(remotesite)         # 连接到FTP站点
connection.login(remoteuser, remotepass)    # 用户名/密码登录
connection.cwd(remotedir)                   # 进入待复制目录
if nonpassive:                              # 强制主动FTP模式
    connection.set_pasv(False)             # 多数服务器采用被动模式
if cleanall:
    for remotename in connection.nlst():   # 尝试删除所有远程文件
        try:
            print('deleting remote', remotename)
            connection.delete(remotename)
        except:
            print('cannot delete remote', remotename)

count = 0                                     # 上传所有本地文件
localfiles = os.listdir(localdir)             # 剥除目录路径
for localname in localfiles:
    mimetype, encoding = guess_type(localname)   # 比如('text/plain', 'gzip')
    mimetype = mimetype or '?/?'                 # 可以是(None, None)
    maintype = mimetype.split('/')[0]            # 对于.jpg文件: ('image/jpeg', None)
    localpath = os.path.join(localdir, localname)
    print('uploading', localpath, 'to', localname, end='')
    print('as', maintype, encoding or '')
    if maintype == 'text' and encoding is None:
        # 以ascii模式和文本文件进行传输
        # 使用和ftplib兼容的编码体系
        localfile = open(localpath, 'rb')
        connection.storlines('STOR ' + localname, localfile)
    else:
        # 以二进制模式和字节文件进行传输
        localfile = open(localpath, 'rb')
        connection.storbinary('STOR ' + localname, localfile)
    localfile.close()
    count += 1

connection.quit()
print('Done:', count, 'files uploaded.')
