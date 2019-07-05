import os
import time


def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)                     # 让父进程等待
        msg = ('Spam %03d' % zzz).encode()  # 管道是二进制字节
        os.write(pipeout, msg)               # 发送到父进程
        zzz = (zzz+1) % 5                   # 0 -> 4


def parent():
    pipein, pipeout = os.pipe()               # 创建带有两个末端的管道
    if os.fork() == 0:                      # 复制此进程
        child(pipeout)                       # 在副本中运行child
    else:                                   # 在父进程中监听管道
        while True:
            line = os.read(pipein, 32)        # 数据发送完之前保持阻塞
            print('Parent %d got [%s] at %s' % (os.getpid(), line, time.time()))

parent()