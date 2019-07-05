"""分支出子进程，直到输入'q'"""

import os


def child():
    print('Hello from child', os.getpid())
    os._exit(0)                             # 否则将回到父循环中


def parent():
    while True:                           # 在父进程中返回新子进程的ID
        newpid = os.fork()                  # unix下才有效，win下测试不了
        if newpid == 0:                     # 子进程
            child()
        else:                               # 父进程
            print('Hello from parent', os.getpid(), newpid)
        if input() == 'q':
            break

parent()
