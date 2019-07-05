"""
扩展FtpTools类，从远程目录树删除文件和子目录，也支持嵌套目录，视dir()命令
输出的格式，在某些服务器上可能会不同
"""

from ftptools import FtpTools


class CleanAll(FtpTools):
    """
    删除整个远程目录树中的所有子目录
    """
    def __init__(self):
        self.fcount = self.dcount = 0

    def getlocaldir(self):
        return None          # 此脚本里无关紧要

    def getcleanall(self):
        return True          # 隐式地要求此设置

    def cleandir(self):
        """
        对于当前远程目录的每一项，删除简单的文件，
        递归进入并删除子目录ftp调用dir()将每一行传入一个函数或方法
        """
        lines = []                         # 每层有自己的lines
        self.connection.dir(lines.append)  # 列出当前远程目录
        for line in lines:
            parsed = line.split()          # 在泛空格符处分割字符串
            permiss = parsed[0]            # 假定'drw... ...文件名'格式
            fname = parsed[-1]
            if fname in ('.', '..'):       # 某些文件名包括当前工作目录和上一级目录
                continue
            elif permiss[0] != 'd':        # 简单文件：删除
                print('files', fname)
                self.connection.delete(fname)
                self.fcount += 1
            else:
                print('directory', fname)   # 目录：递归删除
                self.connection.cwd(fname)
                self.cleandir()             # 清空子目录
                self.connection.cwd('..')   # 改变目录，返回远程目录上一级
                self.connection.rmd(fname)  # 删除空的远程目录
                self.dcount += 1
                print('directory exited')

if __name__ == '__main__':
    ftp = CleanAll()
    ftp.configtransfer(site='learning-python.com', rdir='training', user='lutz')
    ftp.run(cleantarget=ftp.cleandir)
    print('Done:', ftp.fcount, 'files and', ftp.dcount, 'directories cleaned.')
