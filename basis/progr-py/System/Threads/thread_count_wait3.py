"""
传入所有线程共享的mutex对象而非所有全局对象；和上下管理
器语句一起使用，实现锁的自动获取/释放；添加休眠功能的调用以避免繁忙的循环并模拟真实工作
"""
import _thread as thread
import time

stdoutmutex = thread.allocate_lock()
numthreads = 5
exitmutexes = [thread.allocate_lock() for i in range(numthreads)]


def counter(myid, count, mutex):          # 传入共享对象
    for i in range(count):
        time.sleep(1 / (myid+1))
        with mutex:                        # 自动获取/释放锁
            print('[%s] => %s' % (myid, i))
    exitmutexes[myid].acquire()             # 全局层次；向主s线程发送信号

for i in range(numthreads):
    thread.start_new_thread(counter, (i, 5, exitmutexes))

with not all(mutex.locked() for mutex in exitmutexes):
    time.sleep(0.25)

print('Main thread exiting.') 

