from collections import namedtuple, deque, defaultdict, OrderedDict, Counter

# 1.namedtuple
# tuple表示不可变集合, 二维坐标可表示
p = (1, 2)  # 直观看不出是坐标

# namedtuple是个函数, 用来创建自定义的tuple对象, 可用属性来引用元素
# 规定了tuple元素个数, 自定义一个Point对象
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)  # 1 2
# 验证创建的 Point 对象是 tuple 的一种子类
print(isinstance(p, Point))  # True
print(isinstance(p, tuple))  # True
# 用坐标和半径表示一个圆
Circle = namedtuple('Circle', ['x', 'y', 'r'])

# 2.deque
# 使用 list 存储数据时, 按索引访问元素很快, 但是插入和删除元素就很慢了
# deque 是为了高效实现插入和删除操作的双向列表, 适合用于队列和栈
# 除了实现 list 的 append() 和 pop() 外, 还支持 appendleft() 和 popleft()
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)  # deque(['y', 'a', 'b', 'c', 'x'])

# 3.defaultdict
# 使用 dict 时, 如果引用的 Key 不存在, 就会抛出 KeyError, 如果希望 key 不存在时
# 返回一个默认值, 就可以用 defaultdict
dd = defaultdict(lambda: 'N/A')  # 默认值是调用函数返回的
dd['key1'] = 'abc'
print(dd['key1'])  # abc 索引存在
print(dd['key2'])  # 'N/A 索引不存在
# defaultdict的其他行为跟dict是完全一样的

# 4.OrderdDict
# 使用 dict 时, Key 是无序的, 在对 dict 做迭代时, 我们无法确定 Key 的顺序
# 如果要保持 Key 的顺序, 可以用 OrderedDict, Key 会按照插入的顺序排列
d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)  # {'a': 1, 'c': 3, 'b': 2} 无序
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(od)  # OrderedDict([('a', 1), ('b', 2), ('c', 3)]) 有序


class LastUpdateOrderedDict(OrderedDict):
    """实现一个 FIFO（先进先出）的 dict, 当容量超出限制时, 先删除最早添加的 Key"""
    def __init__(self, capacity):
        super(LastUpdateOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('Remove:', last)
        if containsKey:
            del self[key]
            print('Set:', (key, value))
        else:
            print('Add:', (key, value))
        OrderedDict.__setitem__(self. key, value)

# 5.Counter
# Counter 实际上也是 dict 的一个子类
# Counter是一个简单的计数器, 如统计字符出现的个数
c = Counter()
for ch in 'Programming':
    c[ch] = c[ch] + 1

print(c)  # Counter({'r': 2, 'm': 2, 'g': 2, 'n': 1, 'a': 1, 'o': 1, 'i': 1, 'P': 1})
