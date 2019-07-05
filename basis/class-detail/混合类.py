from lister import *


class Super(object):
    def __init__(self):
        self.data1 = 'spam'

    def ham(self):
        pass


class Sub1(Super, ListInstance):
    def __init__(self):
        Super.__init__(self)
        self.data2 = 'eggs'
        self.data3 = 42

    def spam(self):
        pass


class Sub2(Super, ListInherited):
    def __init__(self):
        Super.__init__(self)
        self.data2 = 'eggs'
        self.data3 = 42

    def spam(self):
        pass


class Sub3(Super, ListTree):
    def __init__(self):
        Super.__init__(self)
        self.data2 = 'eggs'
        self.data3 = 42

    def spam(self):
        pass

if __name__ == '__main__':
    # X = Sub1()
    # If using __repr__, Sub2 will recurse.
    # X = Sub2()
    X = Sub3()
    print(X)
