# 匿名管道和线程而非进程；这个版本可以在Windows上工作

import os
import time
import threading


def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)                      # 让父进程等待
        msg = ('Spam %03d'% zzz).encode()    # 管道是二进制字节
        os.write(pipeout, msg)               # 发送到父进程
        zzz = (zzz+1) % 5                    # 0 -> 4


def parent(pipein):
    while True:
        line = os.read(pipein, 32)           # 数据发送完之前保持阻塞
        print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

pipein, pipeout = os.pipe()
threading.Thread(target=child, args=(pipeout,)).start()
parent(pipein)