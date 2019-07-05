"""
itertools提供了非常有用的用于操作迭代对象的函数。
首先，我们看看itertools提供的几个“无限”迭代器

itertools 模块提供的全部是处理迭代功能的函数，它们的返回值不是list，
而是Iterator，只有用for循环迭代的时候才真正计算
"""
import itertools

# 1.count()
# count()会创建一个无限的迭代器
natuals = itertools.count(1)
for n in natuals:
    print(n)  # 不会停
"""...
1
2
3
...
"""

# 2.cycle
# cycle() 会把传入的一个序列无限重复下去
cs = itertools.cycle('ABC')
for c in cs:
    print(c)  # 不会停
"""'A'
'B'
'C'
'A'
'B'
'C'
...
"""

# 3.repeat()
# 把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数
ns = itertools.repeat('A', 3)  # 3次
for n in ns:
    print(n)
"""
...
A
A
A
"""

# 4.takewhile
# 限序列虽然可以无限迭代下去, 我们可以通过takewhile函数截取出一个有限的序列
natuals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, natuals)
list(ns)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 5.chain()
# 把一组迭代对象串联起来，形成一个更大的迭代器
for c in itertools.chain('ABC', 'XYZ'):
    print(c)  # 迭代效果：'A' 'B' 'C' 'X' 'Y' 'Z'

# 6.groupby()
# 把迭代器中相邻的重复元素挑出来放在一起
for key, group in itertools.groupby('AAABBBCCAAA'):
    print(key, group)
"""
A ['A', 'A', 'A']
B ['B', 'B', 'B']
C ['C', 'C']
A ['A', 'A', 'A']
"""

# 实际上挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等
# 这两个元素就被认为是在一组的
# 如果要忽略大小写分组，可以让元素'A'和'a'都返回相同的key
for key, group in itertools.groupby('AaaBBbcCAAa', lambda c: c.upper()):
    print(key, list(group))
"""
A ['A', 'a', 'a']
B ['B', 'B', 'b']
C ['c', 'C']
A ['A', 'A', 'a']

"""


def pi(N):
    """计算这个序列的前N项和 -- 计算pi的值"""
    s1 = (i for i in itertools.count(1) if i % 2 != 0)
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
    s2 = itertools.takewhile(lambda x: x <= 2*N - 1, s1)
    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
    tag1 = 1
    s3 = []
    for i in s2:
        s3.append(tag1 * 4 / i)
        tag1 = tag1 * (-1)
    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...
    s4 = sum(s3)
    # step 4: 求和:
    return s4

# 测试:
print(pi(10))
print(pi(100))
print(pi(1000))
print(pi(10000))
assert 3.04 < pi(10) < 3.05
assert 3.13 < pi(100) < 3.14
assert 3.140 < pi(1000) < 3.141
assert 3.1414 < pi(10000) < 3.1415
print('ok')


def pi2(N):
    """计算这个序列的前N项和 -- 计算pi的值"""
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
    pi = itertools.count(1, 2)
    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
    pi = itertools.takewhile(lambda x: x <= 2 * N - 1, pi)
    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...
    zf = itertools.cycle([+4, -4])
    # step 4: 求和:
    return sum(next(zf) / next(pi) for x in range(N)


def init_odd():
    """生成奇数"""
    n = 1
    while True:
        yield n
        n = n + 2

# 生成4、-4
natural_num = itertools.count(1)
def operate(num):
    n = next(natural_num)
    if n % 2 != 0:
        return 4 / num
    else:
        return -4 / num

def pi3(N):
    """计算这个序列的前N项和 -- 计算pi的值"""
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
    o = init_odd()
    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
    odd_n = itertools.takewhile(lambda x: x <= 2*N-1, o)
    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...
    map_n = map(operate, odd_n)
    # step 4: 求和:
    result = reduce(lambda x, y: x + y, map_n)
    return result
