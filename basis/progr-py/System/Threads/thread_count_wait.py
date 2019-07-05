"""
使用mutexes在父/主线程中探知线程何时结束，而不再
使用time.sleep；给stdout加锁以避免混杂在一起的打印；
"""

import _thread as thread

stdoutmutex = thread.allocate_lock()
exitmutexes = [thread.allocate_lock() for i in range(10)]


def counter(myid, count):                   # 线程中运行的函数
    for i in range(count):
        stdoutmutex.acquire()
        print('[%s] => %s' % (myid, i))       # print函数现在不再被打断了
        stdoutmutex.release()
    exitmutexes[myid].acquire()               # 向主线程发信号

for i in range(10):
    thread.start_new_thread(counter, (i, 100))

for mutex in exitmutexes:
    while not mutex.locked():
        pass

print('Main thread exiting.')