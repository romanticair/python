"""
扩展FtpTools类，将本地目录树中所有文件和子目录上传至远程站点/目录，也支持
嵌套目录，但不支持cleanall选项（这要求解析FTP列表以探测远程目录：参考claenall.py）
为上传子目录，请使用os.path.isdir(path)查看本地文件是否为目录，用FTP().mkd(path)
在远程计算机上创建目录（封装在try语句中以防目录已经存在)，并且递归上传嵌套子目录
中所有的文件/目录
"""

import os
import ftptools


class UploadAll(ftptools.FtpTools):
    """
    上传整个目录树中所有子目录
    假定存在顶层远程目录
    """
    def __init__(self):
        self.fcount = self.dcount = 0

    def getcleanall(self):
        return False

    def uploaddir(self, localdir):
        localfiles = os.listdir(localdir)
        for localname in localfiles:
            localpath = os.path.join(localdir, localname)
            print('uploading', localpath, 'to', localname, end=' ')
            if not os.path.isdir(localpath):
                self.uploadone(localname, localpath, localname)
                self.fcount += 1
            else:
                try:
                    self.connection.mkd(localname)
                    print('directory created')
                except:
                    print('directory not created')
                self.connetion.cwd(localname)          # 修改远程目录
                self.uploaddir(localpath)              # 递归上传本地子目录
                self.connection.cwd('..')              # 返回上级目录
                self.dcount += 1
                print('directory exited')

if __name__ == '__main__':
    ftp = UploadAll()
    ftp.configtransfer(site='learning-python.com', rdir='training', user='lutz')
    ftp.run(transferact=lambda: ftp.uploaddir(ftp.localdir))
    print('Done:', ftp.fcount, 'files and', ftp.dcount, 'directories uploaded.')
