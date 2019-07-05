"""
分支子进程，用os.wait观察其退出状态；分支在Unix和Cygwin下能够进行，
但在Windows Python标准版本中不行；请注意：派生线程共享全局变量，
但每个分支进程拥有其自己的全局变量副本（分支共享文件描述符）；
exitstat在这里将保持不变，而如果是线程的话讲发生变化。
"""
import os

exitstat = 0


def child():
    global exitstat
    exitstat += 1                                     # 更改这个进程的全局变量
    print('Hello from child', os.getpid(), exitstat)  # 发送到父进程的wait函数的退出状态
    os._exit(exitstat)                                # 这里可以调用os.exit
    print('Never reached')


def parent():
    while True:                                      # 持续循环，直到控制台输入'q'
        newpid = os.fork()                            # 开始进程的副本
        if newpid == 0:                               # 如果是在副本中，运行子进程逻辑业务
            child()
        else:
            pid, status = os.wait()
            print('Parent got', pid, status, (status >> 8))
            if input() == 'q':
                break

if __name__ == '__main__':
    parent()