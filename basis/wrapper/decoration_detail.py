from functools import wraps


def decorator_name(f):
    @wraps(f)
    # 接受一个函数进行装饰,并加入了复制函数名字,注释文档,
    # 参数列表等功能,让我们可在装饰器里访问装饰前的函数的属性
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated


@decorator_name
def func():
    return ("Function is running")

can_run = True
print(func())

can_run = False
print(func())


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + "was called")
        return func(*args, **kwargs)
    return with_logging


@logit
def addition_func(x):
    return x + x

#result = addition_func(4)
#print(result)


def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I'm doing some boring job before executing a_func")

        a_func()

        print("I'm doing some boring job after executimg it")

    return wrapTheFunction


@a_new_decorator
def a_function_requiring_decoration():
    # 主函数
    print("I'm the function which needs some decoration to remove")

a_function_requiring_decoration()
# 在这里，函数被wrapTheFunction替代了，它重写了我们函数的名字和注释文档(docstring)
# print(a_function_requiring_decoration.__name__)
# 我们可以用一个函数functools.wraps解决掉


def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I'm doing some boring job before executing a_func")
        a_func()
        print("I'm doing some boring job after executimg it")

    return wrapTheFunction


@a_new_decorator
def a_function_requiring_decoration():
    # 主函数
    print("I'm the function which needs some decoration to remove")

a_function_requiring_decoration()
print(a_function_requiring_decoration.__name__)


def a_function_requiring_decoration():
    print("I'm the function which needs some decoration to remove")

a_function_requiring_decoration()
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
a_function_requiring_decoration()
