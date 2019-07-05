"""
可创建Process类的子类，就像threading.Thread一样；Queue和queue.Queue
的使用方法类似，不过它不是线程间的工具，而是进程间的工具。
"""

import os
import time
import queue
from multiprocessing import Process, Queue              # 进程安全的共享队列
                                                          # 队列是管道+锁/信号机


class Counter(Process):
    label = ' @'

    def __init__(self, start, queue):                    # 为运行中的用处保留状态
        self.state = start
        self.post = queue
        Process.__init__(self)

    def run(self):
        # 新进程中调用start()时开始运行
        for i in range(3):
            time.sleep(1)
            self.state += 1
            print(self.label, self.pid, self.state)       # self.pid为该子进程的pid
            self.post.put([self.pid, self.state])         # stdout文件为所有进程共享
        print(self.label, self.pid, '-')

if __name__ == '__main__':
    print('start', os.getpid())

    expected = 9
    post = Queue()
    p = Counter(0, post)                                  # 开始共享队列的3个进程
    q = Counter(100, post)                                # 子进程是生产者
    r = Counter(1000, post)
    p.start()
    q.start()
    r.start()
    while expected:                                      # 父进程消耗队列中的数据
        time.sleep(0.5)                                   # 本质上来说，这像一个GUI
        try:                                              # 虽然GUI通常使用线程
            data = post.get(block=False)
        except queue.Empty:
            print('no data...')
        else:
            print('posted:', data)
            expected -= 1

    p.join()
    q.join()
    r.join()                                              # 必须在join put之前进行
    print('finish', os.getpid(), r.exitcode)              # exitcode是子进程退出状态



