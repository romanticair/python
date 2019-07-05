"""
Climb inheritance trees using namespace links,
displaying higher superclasses with indentation
"""


def class_tree(cls, indent):
    print('.' * indent + cls.__name__)
    for supercls in cls.__bases__:
        class_tree(supercls, indent+3)


def instance_tree(inst):
    print('Tree of %s' % inst)
    class_tree(inst.__class__, 3)


def self_test():
    class A:pass
    class B(A): pass
    class C(A): pass
    class D(B, C): pass
    class E: pass
    class F(D, E): pass
    instance_tree(B())
    instance_tree(F())


if __name__ == '__main__':
    self_test()
