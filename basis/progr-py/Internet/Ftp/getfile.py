"""
通过FTP抓取任意文件，默认使用匿名FTP，除非传入了一个user=(name, pswd)元组，利用
一个测试文件和站点进行自测。
"""
from ftplib import FTP
from os.path import exists                    # 检查文件是否存在


def getfile(file, site, dir, user=(), *, verbose=True, refetch=False):
    """
    通过ftp站点或目录中获取文件，
    匿名或账号登录，二进制传输
    """
    if exists(file) and not refetch:
        if verbose:
            print(file, 'already fetched')
    else:
        if verbose:
            print('Downloading', file)
            local = open(file, 'wb')           # 同名的本地文件
        try:
            remote = FTP(site)                 # 连接FTP站点
            remote.login(*user)                # ()代表匿名登录，或者使用(name, pswd)
            remote.cwd(dir)
            remote.retrbinary('RETR ' + file, local.write, 1024)
            remote.quit()
        finally:
            local.close()                      # 无论如何都关闭文件
        if verbose:
            print('Download done.')

if __name__ == '__main__':
    from getpass import getpass
    file = 'monkeys.jpg'
    dir = '.'
    site = 'ftp.rmi.net'
    user = ('lutz', getpass('Pswd'))
    getfile(file, site, dir, user)
