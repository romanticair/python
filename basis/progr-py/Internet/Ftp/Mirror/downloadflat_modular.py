"""
使用FTP从远程站点和目录将所有文件复制（下载）到本地计算机上的目录，这一版运行方式
相同，但依旧经过重构，代码被封装在函数中，后者能够被上传脚本及将来其他可能的程序复用，
否则将导致代码冗余，而后者要么随时间推移导致版本分歧，要么使代码维护成本翻倍。
"""
import os
import sys
import ftplib
from getpass import getpass
from mimetypes import guess_type, add_type

defaultSite = 'home.rmi.net'
defaultRdir = '.'
defaultUser = 'lutz'


def config_transfer(site=defaultSite, rdir=defaultRdir, user=defaultUser):
    """
    获取上传或下载参数
    由于处理数量较大，使用类来完成
    """
    class cf:
        pass
    cf.nonpassive = False
    cf.remotesite = site
    cf.remotedir = rdir
    cf.remoteuser = user
    localdir = (len(sys.argv) > 1 and sys.argv[1]) or '.'
    cleanall = input('Clean remote directory first? ')[:1] in ['y', 'Y']
    remotepass = getpass('Password for %s on %s: ' % (cf.remoteuser, cf.remotesite))
    return cf


def is_text_kind(remotename, trace=True):
    """
    借助Mimetype猜测文件名代表文本还是二进制
    对于文件'f.html'，猜测结果是('text/html', None) 文本
    对于文件'f.jpeg'，猜测结果是('image/jpeg', None) 二进制
    对于文件'f.txt.gz'，猜测结果是('text/plain', 'gzip') 二进制
    对于未知类型，猜测结果可能是(None, None) 二进制
    mimtetype还能根据文件类型猜测名称：参考PyMailGUI
    """
    add_type('text/x-python-win', '.pyw')                         # 不在表格中
    mimetype, encoding = guess_type(remotename, strict=False)    # 接受额外类型
    mimetype = mimetype or '?/?'                                  # 类型未知
    maintype = mimetype.split('/')[0]                             # 获取第一部分
    if trace:
        print(maintype, encoding or '')
    return maintype == 'text' and encoding is None              # 文件未压缩


def connect_ftp(cf):
    print('connecting...')
    connection = ftplib.FTP(cf.remotesite)           # 连接到FTP站点
    connection.login(cf.remoteuser, cf.remotepass)   # 用户名/密码登录
    connection.cwd(cf.remotedir)                     # 进入待复制目录
    if cf.nonpassive:                                # 强制主动FTP模式
        connection.set_pasv(False)                  # 多数服务器采用被动模式
    return connection


def clean_locals(cf):
    """
    试图首先删除所有本地文件以清除垃圾文件
    """
    if cf.cleanall:
        for localname in os.listdir(cf.localdir):  # 获取本地目录列表
            try:
                print('deleting local', localname)  # 删除本地文件
                os.remove(os.path.join(cf.localdir, localname))
            except:
                print('connot delete local', localname)


def download_all(cf, connection):
    """
    按照cf配置从远程站点/目录下载所有文件
    fpt的nlst()给出文件列表，dir()给出全部细节
    """
    remotefiles = connection.nlst()
    for remotename in remotefiles:
        if remotename in ('.', '..'):
            continue
        localpath = os.path.join(cf.localdir, remotename)
        print('downloading', remotename, 'to', localpath, end='')
        if is_text_kind(remotename):
            # 以文本文件进行传输
            localfile = open(localpath, 'w', encoding=connection.encoding)
            callback = lambda line: localfile.write(line + '\n')
            connection.retrlines('RETR ' + remotename, callback)
        else:
            # 以二进制模式进行传输
            localfile = open(localpath, 'wb')
            connection.retrbinary('RETR ' + remotename, localfile.write)
        localfile.close()
    connection.quit()
    print('Done:', len(remotefiles), 'files downloaded.')

if __name__ == '__main__':
    cf = config_transfer()
    conn = connect_ftp(cf)
    clean_locals(cf)        # 没连接上就不删除
    download_all(cf, conn)












