import _thread


def action(i):                                    # 线程中运行的函数
    print(i ** 32)                                 # 3个线程都打印同一数字


class Power:
    def __init__(self, i):
        self.i = i

    def action(self):                             # 线程中运行的绑定方法
        print(self.i ** 32)


_thread.start_new_thread(action, (2,))              # 简单函数
_thread.start_new_thread(lambda: action(2), ())    # 待执行的lambda函数
obj = Power(2)
_thread.start_new_thread(obj.action, ())            # 绑定方法对象 