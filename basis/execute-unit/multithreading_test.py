"""
下面的案例有
1. 单、多线程
2. 加锁单、多线程
3. 死循坏测试
"""

import time
import threading
from threading import Lock
import multiprocessing

balance = 0
lock = Lock()  # 给线程加锁


def loop():
    # 线程执行的代码
    print("Theading %s is running..." %threading.current_thread().name)  # 子线程
    n = 0
    while n < 5:
        n = n + 1
        print("Threading %s >>> %d" %(threading.current_thread().name, n))
        time.sleep(1)

    print("Thread %s is ended..." %threading.current_thread().name)


def loop_tt():
    print("Thread %s is running..." %threading.current_thread().name)
    t = threading.Thread(target=loop, name='Loop_Thread_Tt')
    t.start()
    t.join()
    print("Thread %s is ended..." %threading.current_thread().name) # 主线程


def change_it(n):
    # 多线程要执行的代码
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread1(n):
    # 加锁多线程
    for i in range(1000):
        # 获取锁
        lock.acquire()
        try:
            change_it(i)
        finally:
            lock.release() # 无论如何都释放锁, 以免造成死线程


def run_thread2(n):
    # 不加锁
    for i in range(100000):
        change_it(n)


def run_thread_tt():
    # 测试
    t1 = threading.Thread(target=run_thread1, args=(5,))
    t2 = threading.Thread(target=run_thread1, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)


def core_dead():
    # 死循环测试
    def loop():
        x = 0
        while True:
            x = x * 1

    for i in range(multiprocessing.cpu_count()):
        t1 = threading.Thread(target=loop)
        t2 = threading.Thread(target=loop)
        t1.start()
        t2.start()


if __name__ == '__main__':
    # loop_tt()
    # run_thread_tt()
    core_dead()
