"""
zip 文件字典法多线程暴力破解

提高性能，多线程测试多个口令(单词)
为使用户可以指定要破解的Zip文件的文件名和字典文件的文件名，导入 optparse 库

-- 尚未解决找到密码后立即结束其它线程的工作 ???
加入 Event，找到密码立即清除掉所有线程？？
"""

import zipfile
import optparse
from sys import exit
from threading import Thread, Event


def extract_file(z_file, password):
    """
    :param z_file: 需要破解的文件
    :param password: 字典密码
    """
    try:
        #event.wait()
        z_file.extractall(pwd=password.encode('utf-8'))
        print('[+] Password is {0}'.format(password))
        #event.clear()
        exit(0)
    except Exception:
        pass


def main():
    parser = optparse.OptionParser("usage %prog -f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',
                      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',
                      help='specify dictionary file')
    (options, args) = parser.parse_args()
    if options.zname is None or options.dname is None:
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    z_file = zipfile.ZipFile(zname)
    p_file = open(dname)
    for line in p_file.readlines():
        password = line.strip('\n')
        t = Thread(target=extract_file, args=(z_file, password))
        t.start()
        #event.set()

if __name__ == '__main__':
    #event = Event()
    main()
    # violence_decrypt.py -f evil.zip -d dictionary.txt
