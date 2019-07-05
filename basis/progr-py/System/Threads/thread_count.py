"""
线程基本操作：并行地启用5个函数副本；利用time.sleep避免主线程
过早退出，这样在某些系统平台上将导致其它线程终止；共享stdout:
线程输出在这个版本里可能随机混合在一起。
"""
import _thread as thread
import time


def counter(myid, count):                   # 线程中运行的函数
    for i in range(count):
        time.sleep(1)                         # 模拟真实工作
        print('[%s] => %s' % (myid, i))


for i in range(5):                           # 派生五个子线程
    thread.start_new_thread(counter, (i, 5))  # 每个线程中循环5次

time.sleep(6)
print('Main thread exting.')