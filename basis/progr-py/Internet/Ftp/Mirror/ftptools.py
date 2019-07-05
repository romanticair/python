"""
############################################################################################
使用FTP从/向远程站点和目录下载或上传单个目录下所有文件，这一版本经过重构，以便使用类和
OOP以获得命名空间和自然的结构；我们还可以把这个脚本构建成下载超类，以及可以重新定义清除
和传输方法的上传超类，不过那样的话，对于别的客户程序一起调用上传和下载来说不太方便；对于
uploadedall和其它可能的变异版本，还需在最初的循环方法中加上单个文件上传/下载代码；
############################################################################################
"""

import os
import sys
import ftplib
from getpass import getpass
from mimetypes import guess_type, add_type


# 所有客户程序的默认设置
dfltSite = 'home.rmi.net'
dfltRdir = '.'
dfltUser = 'lutz'


class FtpTools:
    # 运行下面这3个工具被重新定义

    def getlocaldir(self):
        return (len(sys.argv) > 1 and sys.argv[1]) or '.'

    def getcleanall(self):
        return input('Clean target dir first?')[:1] in ['y', 'Y']

    def getpassword(self):
        return getpass('Password for %s on %s' % (self.remoteuser, self.remotesite))

    def configtransfer(self, site=dfltSite, rdir=dfltRdir, user=dfltUser):
        """
        从模块默认设置、参数、输入、命令行获取上传或下载参数
        匿名fpt: user='anoymous' pass=emailaddr
        """
        self.nonpassive = False
        self.remotesite = site
        self.remotedir = rdir
        self.remoteuser = user
        self.localdir = self.getlocaldir()
        self.cleanall = self.getcleanall()
        self.remotepass = self.getpassword()

    def istextkind(self, remotename, trace=True):
        """
        借助Mimetype猜测文件名代表文本还是二进制
        对于文件'f.html'，猜测结果是('text/html', None) 文本
        对于文件'f.jpeg'，猜测结果是('image/jpeg', None) 二进制
        对于文件'f.txt.gz'，猜测结果是('text/plain', 'gzip') 二进制
        对于未知类型，猜测结果可能是(None, None) 二进制
        mimtetype还能根据文件类型猜测名称：参考PyMailGUI
        """
        add_type('text/x-python-win', '.pyw')                      # 不在表格中
        mimetype, encoding = guess_type(remotename, strict=False)  # 接受额外类型
        mimetype = mimetype or '?/?'                               # 类型未知
        maintype = mimetype.split('/')[0]                           # 获取第一部分
        if trace:
            print(maintype, encoding or '')
        return maintype == 'text' and encoding is None            # 文件未压缩

    def connectftp(self):
        print('connecting...')
        connection = ftplib.FTP(self.remotesite)                # 连接到FTP站点
        connection.login(self.remoteuser, self.remotepass)      # 用户名/密码登录
        connection.cwd(self.remotedir)                          # 进入待复制目录
        if self.nonpassive:                                    # 强制主动FTP模式
            connection.set_pasv(False)                         # 多数服务器采用被动模式
        self.connection = connection

    def cleanlocals(self):
        """
        试图首先删除所有本地文件以清除垃圾文件
        """
        if self.cleanall:
            for localname in os.listdir(self.localdir):  # 获取本地目录列表
                try:
                    print('deleting local', localname)    # 删除本地文件
                    os.remove(os.path.join(self.localdir, localname))
                except:
                    print('connot delete local', localname)

    def cleanremotes(self):
        """
        试图首先删除所有远程文件以清除垃圾文件
        """
        if self.cleanall:
            for remotename in self.connection.nlst():    # 尝试删除所有远程文件
                try:
                    print('deleting remote', remotename)
                    self.connection.delete(remotename)
                except:
                    print('cannot delete remote', remotename)

    def downloadone(self, remotename, localpath):
        """
        通过FTP以文本或二进制模式下载单个文件
        本地文件名无须与远程名相同
        """
        if self.istextkind(remotename):
            localfile = open(localpath, 'w', encoding=self.connection.encoding)
            def callback(line):
                localfile.write(line + '\n')
            self.connection.retrlines('RETR ' + remotename, callback)
        else:
            localfile = open(localpath, 'wb')
            self.connection.retrbinary('RETR ' + remotename, localfile.write)
        localfile.close()

    def uploadone(self, localname, localpath, remotename):
        """
        通过FTP以文本或二进制模式上传单个文件
        本地文件名无须与远程名相同
        """
        if self.istextkind(localname):
            localfile = open(localpath, 'rb')
            self.connection.storlines('STOR ' + remotename, localfile)
        else:
            localfile = open(localpath, 'rb')
            self.connection.retrbinary('RETR ' + remotename, localfile)
        localfile.close()

    def downloaddir(self):
        """
        按照cf配置从远程站点/目录下载所有文件
        fpt的nlst()给出文件列表，dir()给出全部细节
        """
        remotefiles = self.connection.nlst()
        for remotename in remotefiles:
            if remotename in ('.', '..'):
                continue
            localpath = os.path.join(self.localdir, remotename)
            print('downloading', remotename, 'to', localpath, end='')
            self.downloadone(remotename, localpath)
        print('Done:', len(remotefiles), 'files downloaded.')

    def uploaddir(self):
        """
        按照配置将所有文件上传到远程站点/目录
        listdir()剥去了目录路径，任何操作失败都将终端脚本
        """
        localfiles = os.listdir(self.localdir)
        for localname in localfiles:
            localpath = os.path.join(self.localdir, localname)
            print('updateing', localpath, 'to', localname, end='')
            self.uploadone(localname, localpath, localname)
        print('Done:', len(localfiles), 'files uploaded.')

    def run(self, cleantarget=lambda: None, transferact=lambda: None):
        """
        运行一个完整的FTP会话
        默认不进行清除和传输
        没连接上服务器时不要删除
        """
        self.connectftp()
        cleantarget()
        transferact()
        self.connection.quit()

if __name__ == '__main__':
    ftp = FtpTools()
    xfermode = 'download'
    if len(sys.argv) > 1:
        xfermode = sys.argv.pop(1)     # 获取和删除第二个参数
    if xfermode == 'download':
        ftp.configtransfer()
        ftp.run(cleantarget=ftp.cleanlocals, transferact=ftp.downloaddir)
    elif xfermode == 'upload':
        ftp.configtransfer(site='learning-python.com', rdir='books', user='lutz')
        ftp.run(cleantarget=ftp.cleanremotes, transferact=ftp.uploadone)
    else:
        print('Usage: ftptools.py ["download" | "upload"] [localdir]')
