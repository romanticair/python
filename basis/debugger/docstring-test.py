# 代码在注释中, 由一些工具来自动生成文档, 可自动执行写在注释中的代码
# Python内置的“文档测试” doctest 模块可以直接提取注释中的代码并执行测试
# doctest 严格按照 Python 交互式命令行的输入和输出来判断测试结果是否正确
# 只有测试异常的时候，可以用...表示中间一大段烦人的输出
# 下面写三个例子用来测试


def my_abs(n):
    '''
    Function to get absolute value of number.
    Example:

    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    '''
    return n if n >= 0 else (-n)


def fact(n):
    '''
    Calculate 1*2*...*n
    Example:

    >>> fact(1)
    1
    >>> fact(10)
    3628800
    >>> fact(-2)
    Traceback (most recent call last):
        ...
    ValueError: -2 is not a value error
    '''
    if n < -1:
        raise ValueError("%d is not a value error" % n)
    if n == 1:
        return 1
    return n * fact(n - 1)


class Dict(dict):
    '''
    Simple dict but also support access as x.y style.
    Example:

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''

    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

# 当模块正常导入时，doctest不会被执行。只有在命令行直接运行时，才执行 doctest， 不必担心 doctest 会在非测试环境下执行
if __name__ == '__main__':
    import doctest
    doctest.testmod()
