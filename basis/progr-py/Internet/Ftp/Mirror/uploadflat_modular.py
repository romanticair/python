"""
使用FTP向远程站点/目录上传本地目录下所有文件，为避免代码冗余，这个
版本复用了下载脚本的函数；
"""
import os
from downloadflat_modular import config_transfer, connect_ftp, is_text_kind


def clean_remotes(cf, connection):
    """
    试图首先删除所有远程文件以清除垃圾文件
    """
    if cf.cleanall:
        for remotename in connection.nlst():           # 尝试删除所有远程文件
            try:
                print('deleting remote', remotename)
                connection.delete(remotename)
            except:
                print('cannot delete remote', remotename)


def update_all(cf, connection):
    localfiles = os.listdir(cf.localdir)    # 剥除目录路径
    for localname in localfiles:
        localpath = os.path.join(cf.localdir, localname)
        print('updateing', localpath, 'to', localname, end='')
        if is_text_kind(localname):
            # 以ascii模式和文本文件进行传输
            localfile = open(localpath, 'rb')
            connection.storlines('STOR ' + localname, localfile)
        else:
            # 以二进制模式和字节文件进行传输
            localfile = open(localpath, 'rb')
            connection.storbinary('STOR ' + localname, localfile)
        localfile.close()
    connection.quit()
    print('Done:', len(localfiles), 'files uploaded.')

if __name__ == '__main__':
    cf = config_transfer(site='learning-python.com', rdir='books', user='lutz')
    conn = connect_ftp(cf)
    clean_remotes(cf, conn)
    update_all(cf, conn)
