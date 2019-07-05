"""
命名管道：os.mkfifo在Windows下不能用；这里没有分支的必要；
因为fifo文件管道对于进程为外部文件--------父进程/子进程
中共享文件描述符在这里没有效果
"""

import os
import time
import sys

fifoname = '/tmp/pipefifo'                       # 必须打开同名文件


def child():
    pipeout = os.open(fifoname, os.O_WRONLY)     # 作为文件描述符打开fifo
    zzz = 0
    while True:
        time.sleep(zzz)
        msg = ('Spam %03d\n' % zzz).encode()     # 此处打开的是二进制字符
        os.write(pipeout, msg)
        zzz = (zzz+1) % 5


def parent():
    pipein = open(fifoname, 'r')                 # 作为文本文件对象打开fifo
    while True:
        line = pipein.readline()[:-1]            # 数据发送完之前保持阻塞
        print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

if __name__ == '__main__':
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)                      # 创建一个具名管道文件
    if len(sys.argv) == 1:
        parent()                                 # 如果没有参数则作为父进程运行
    else:                                       # 否则子进程
        child()



