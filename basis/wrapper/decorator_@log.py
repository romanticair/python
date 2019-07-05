"""
1.设计一个decorator，它可作用于任何函数上，并打印该函数的执行时间
2.请编写一个decorator，能在函数调用的前后打印出'begin call'和'end call'的日志
"""
import time
import functools


def metric(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = fn(*args, **kwargs)
        end = time.time()
        print('%s executed in %s ms' % (fn.__name__, end - start))
        return ret
    return wrapper


@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y


@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z


f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')


def log(text=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if text is not None:
                print("%s %s"%(text, func.__name__))
            else:
                print("%s no text."%func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 写出一个@log的decorator使它既支持 f1, 又支持 f2


@log()
def f1():
    print("I'm f1")


@log('execute')
def f2():
    print("I'm f2")

f1()
log()(f1)()  # equal to f1()
f2()
