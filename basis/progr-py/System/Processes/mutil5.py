"""使用mutiprocessing起始新程序，不论os.fork是否可用"""

import os
from multiprocessing import Process


def run_programm(arg):
    os.execlp('python', 'python', 'child.py', str(arg))

if __name__ == '__main__':
    # 主进程结束，子进程也更着结束了
    for i in range(5):
        p = Process(target=run_programm, args=(i,))
        p.start()
    print('Parent exit.')