class Adder(object):
    def __init__(self, start=[]):
        self.data = start

    def add(self, y):
        print("Not Implemented")

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)


class ListAdder(Adder):
    def add(self, y):
        return self.data + y


class DictAdder(Adder):
    def add(self, x, y):
        new = {}
        for k in x.keys():
            new[k] = x[k]

        for k in y.keys():
            new[k] = y[k]

        return new