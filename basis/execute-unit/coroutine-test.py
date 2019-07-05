"""
协程，又称微线程，纤程。英文名Coroutine

因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，既充分利用多核，
又充分发挥协程的高效率，可获得极高的性能。
Python对协程的支持是通过generator实现的

在generator中，不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句
返回的下一个值。
Python的yield不但可以返回一个值，它还可以接收调用者发出的参数

如生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，
切换回生产者继续生产，效率极高：
"""


def consume():
    """
    I'm a generator
    通过 yield 拿到消息处理，又通过yield把结果传回
    produce拿到consumer处理的结果，继续生产下一条消息；
    produce决定不生产了，通过c.close()关闭 consumer，整个过程结束
    整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务
    """
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)  # 这里传入参数None相当于调用了.next()
    # c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)

    c.close()

if __name__ == '__main__':
    c = consume()
    produce(c)
