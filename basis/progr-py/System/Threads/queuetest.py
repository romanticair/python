"""生产者和消费者线程与共享队列进行通信"""

import _thread as thread
import queue
import time

numconsumers = 2                    # 准备开始的消费者线程的数目
numproducers = 4                    # 准备开始的生产者线程的数目
nummessages = 4                     # 每个生产者存入的消息的数量

safeprint = thread.allocate_lock()  # 否则打印操作可能发生交叠
dataqueue = queue.Queue()           # 共享的全局变量，大小无限


def producer(idnum):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataqueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))


def consumer(idnum):
    while True:
        time.sleep(0.1)
        try:
            data = dataqueue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numproducers):
        thread.start_new_thread(producer, (i,))

    for i in range(numconsumers):
        thread.start_new_thread(consumer, (i,))

    time.sleep((numproducers - 1) * nummessages + 1)
    print('Main thread exit.')
