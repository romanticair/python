"""同步化对stdout的访问：因为stdout为共享的全局对象，
线程输出如果不做同步化可能会交互混杂在一起"""

import _thread as thread
import time


def counter(myid, count):                   # 线程中运行的函数
    for i in range(count):
        time.sleep(1)                         # 模拟真实工作
        mutex.acquire()
        print('[%s] => %s' % (myid, i))       # print函数现在不再被打断了
        mutex.release()

mutex = thread.allocate_lock()                # 创建全局锁对象
for i in range(5):
    thread.start_new_thread(counter, (i, 5))

time.sleep(6)                                 # 避免过早退出