class MyList(list):
    NumInstances = 0

    def __init__(self, x):
        # self.wrapped = x[:]  Copy x: no side effects
        self.wrapped = [i for i in x]
        MyList.NumInstances += 1

    def __add__(self, other):
        return MyList(self.wrapped + other)

    def __mul__(self, other):
        return MyList(self.wrapped * other)

    def __getitem__(self, item):
        print('Your operation: %s' % item)
        return self.wrapped[item]

    def __len__(self, other):
        return len(self.wrapped)

    def append(self, p_object):
        self.wrapped.append(p_object)

    def __getattr__(self, item):
        return getattr(self.wrapped, item)

    def __repr__(self):
        return repr(self.wrapped)

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        if self.i >= len(self.wrapped):
            raise StopIteration

        return self.wrapped[self.i]

    # def sort(self, key=None, reverse=False):
    #     self.wrapped.sort()

    def reverse(self):
        self.wrapped.reverse()

    def __contains__(self, item):
        return item in self.wrapped

    @staticmethod
    def printNumInstances():
        print("Number of instances created: ", MyList.NumInstancess)


if __name__ == '__main__':
    x = MyList('spam')
    y = MyList([1, 5, 3])
    print(MyList.NumInstances)
    print(y.printNumInstances())

    print(x)
    print(x[2])
    print(x[1:])
    print(x + ['eggs'])
    print(x * 3)
    x.append('a')
    x.sort(reverse=True)
    # print('s' in x)
    # x.reverse()
    print(x)
    for c in x:
        print(c, end=', ')




