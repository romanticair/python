from multiprocessing import Process
from multiprocessing import Queue  # 进程间通信
from multiprocessing import Pool
import os
import time
import random
# subprocess 启动子进程模块, 在这里不写


def say_hello(name):
    print('hello ! I\'m child <%s> process ID(%s)...' % (name, os.getpid()))


def processing_test():
    # 单进程练习
    print("I'm parents process ID(%s)" % os.getpid())
    p = Process(target=say_hello, args=('Whoami',))  # 创建子进程
    print("Child process will start.")
    p.start()
    p.join()  # 等待子进程结束
    print("Child process ended.")


def long_time_task(name):
    print("Run task process %s ID(%s)" % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 2)
    end = time.time()
    print("Task process %s run %.2f seconds." % (name, end - start))


def multiprocessing_test():
    # 多进程练习
    print("Parent process ID(%s)." % os.getpid())
    p = Pool(4)  # 同时执行4个子进程
    for i in range(5):
        p.apply_async(long_time_task, args=('subprocess' + str(i),))

    print("Waiting for all subprocesses...")
    p.close() # 不再添加新进程
    p.join() # 等待所有子进程结束
    print("All subprocesses done.")


def write(q):
    # 写数据进程执行的函数
    print("Process to write: %s" % os.getpid())
    for value in ['AAAA', 'BBBB', 'CCCC']:
        print("Put %s to queue..." % value)
        q.put(value)
        time.sleep(random.random())


def read(q):
    # 读数据进程进行的函数
    print("Process to read %s" %os.getpid())
    while True:
        value = q.get(True)
        print("Get %s from queue." %value)


def multiprocess_commu_test():
    # 创建Queue队列, 传给子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动pw, pr进程
    pw.start()
    pr.start()
    # 等待pw结束
    pw.join()
    # 强制终止pr进程(死循坏)
    pr.terminate()
    print("Works done !")


if __name__ == '__main__':
    processing_test()
    print()
    multiprocessing_test()
    print()
    multiprocess_commu_test()
