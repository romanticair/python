"""
multiprocess模块基本操作：Process功能类似threading.Thread，不过在并行
进程而非线程中运行函数调用；可以用锁进行同步化，如某些平台上的打印操作；
在Windows下启动新的解释器，在Unix下分支新进程；
"""
import os
from multiprocessing import Process, Lock


def whoami(label, lock):
    msg = '%s: name:%s, pid:%s'
    with lock:
        print(msg % (label, __name__, os.getpid()))

if __name__ == '__main__':
    lock = Lock()
    whoami('function call', lock)

    p = Process(target=whoami, args=('spaured child', lock))
    p.start()
    p.join()
    for i in range(5):
        Process(target=whoami, args=('run progress %s' % i, lock)).start()

    with lock:
        print('Main process exit.')

