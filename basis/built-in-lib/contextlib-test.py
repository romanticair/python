from contextlib import contextmanager, closing
from urllib.request import urlopen


class file:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("entering")
        self.f = open(self.filename, self.mode)
        return self.f

    def __exit__(self, *args):
        print("will exit")
        self.f.close()

# 因为 File 类实现了上下文管理器，现在就可以使用 with 语句了
with file('out.txt', 'w') as f:
    print("writing")
    f.write('hello, python')

# Python 提供了一个 contextmanager 的装饰器, 进一步简化了上下文管理的实现方式
# 通过 yield 将函数分割成两部分，yield 之前的语句在 __enter__ 方法中执行，之后的
# 语句在 __exit__ 方法中执行，yiled f 中的 f 就是函数的返回值


@contextmanager
def my_open(path, mode):
    f = open(path, mode)
    yield f
    f.close()

# 调用
with my_open('out.txt', 'w') as f:
    f.write("hello , the simplest context manager")


class Query(object):
    """ 实现上下文管理是通过__enter__和__exit__这两个方法实现的 """
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)

# 这样我们就可以把自己写的资源对象用于with语句
with Query('Bob') as q:
    q.query()
# Begin
# Query info about Bob...
# End


class Query(object):
    """
    @contextmanage
    编写__enter__和__exit__仍然很繁琐，因此 Python 的标准库 contextlib 提供了更
    简单的写法，上面的代码可以改写如下：
    """
    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...' % self.name)


@contextmanager
def create_query(name):
    print('Begin')
    q = Query(name)
    yield q
    print('End')

# @contextmanager这个decorator接受一个generator，用yield语句
# 把with ... as var把变量输出出去，然后，with语句就可以正常地工作了
with create_query('Bob') as q:
    q.query
# Begin
# End


@contextmanager
def tag(name):
    # 希望在某段代码执行前后自动执行特定代码，也可以用@contextmanager实现
    print("<%s>" %name)  # 1.with语句首先执行yield之前的语句，因此打印出<h1>
    yield
    print("</%s>" %name)  # 3.最后执行yield之后的语句，打印出</h1>

with tag("h1"):
    print("Hello")  # 2.yield调用会执行with语句内部的所有语句，因此打印出hello和world
    print("world")
# < h1 >
# Hello
# world
# < / h1 >


# @closing
# 如果一个对象没有实现上下文，就不能把它用于with语句。这时
# 可以用closing()来把该对象变为上下文对象。例如，用with语句使用urlopen()
with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)


@contextmanager
def closing(thing):
    # closing 也是一个经过@contextmanager装饰的generator，这
    # 个generator编写起来其实非常简单
    try:
        yield thing
    finally:
        thing.close()
