"""
将任意文件通过FTP在二进制模式下存储。默认使用匿名FTP，除非传入了一个user=(name, pswd)
参数元组。
"""
import ftplib


def putfile(file, site, dir, user=(), *, verbose=True):
    """
    通过ftp将文件保存到站点/目录
    匿名或账号登录，二进制传输
    """
    if verbose:
        print('Uploading', file)
    local = open(file, 'rb')        # 同名的本地文件
    remote = ftplib.FTP(site)       # 连接到FTP站点
    remote.login(*user)             # 匿名或账号登录
    remote.cwd(dir)
    remote.storbinary('STOR ' + file, local, 1024)
    remote.quit()
    local.close()
    if verbose:
        print('Upload done.')

if __name__ == '__main__':
    site = 'ftp.rmi.net'
    dir = '.'
    import sys
    import getpass
    pswd = getpass.getpass(site + ' pswd?')               # 命令行里的文件名
    putfile(sys.argv[1], site, dir, user=('lutz', pswd))  # 非匿名登录
