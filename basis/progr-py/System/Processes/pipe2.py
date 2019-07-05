# 和pipe1.py一样，不过将管道输入封装进stdio文件对象；
# 在两个进程中逐行读取并关闭管道文件描述符

import os
import time


def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)                      # 让父进程等待
        msg = ('Spam %03d\n'% zzz).encode()  # 管道是二进制字节
        os.write(pipeout, msg)               # 发送到父进程
        zzz = (zzz+1) % 5                    # 0 -> 4


def parent():
    pipein, pipeout = os.pipe()              # 创建带有两个末端的管道
    if os.fork() == 0:                       # 在子进程中向管道写入
        os.close(pipein)                     # 在此关闭输入端
        child(pipeout)
    else:                                   # 在父进程中监听管道
        os.close(pipeout)                    # 在此关闭输出端
        pipein = os.fdopen(pipein)           # 创建文本模式的输入文件对象
        while True:
            line = pipein.readline()[:-1]    # 数据发送完之前保持阻塞
            print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

parent()