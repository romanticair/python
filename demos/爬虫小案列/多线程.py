import threading

"""
我们定义一个类并继承threading.Thread类, 将
该类定义为一个线程, 最后我们可以声明多个这样的
类来构建多个线程并通过对应线程对象start()方法启动线程

"""

# 多线程基础

class A(threading.Thread):
    def __init__(self):
        # 初始化化该线程
        threading.Thread.__init__(self)

    def run(self):
        # 该线程要执行的程序内容
        for i in range(100):
            print("我是线程A")


class B(threading.Thread):
    def __init__(self):
        # 初始化化该线程
        threading.Thread.__init__(self)

    def run(self):
        # 该线程要执行的程序内容
        for i in range(100):
            print("我是线程B")


if __name__ == '__main__':
    # 实例化
    t1 = A()
    # 启动线程t1
    t1.start()

    # 实例化
    t2 = B()
    # 启动线程, 此时t1, t2同时进行
    t2.start()
    # 得到穿插输出的结果

    # 队列, FIFO
    import queue

    # 创建一个队列对象
    a = queue.Queue()
    # 将数据传入队列
    a.put("hello")
    # 入队完成
    a.task_done()
    # 出队列
    a.get()













