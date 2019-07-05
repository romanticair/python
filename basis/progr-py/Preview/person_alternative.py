"""
Person类的替代实现，包含数据、行为和运算符重载(未用于对象的持久存储)
"""

class Person:
    """
    一般person: 数据+逻辑
    """
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job

    def last_name(self):
        return self.name.split()[-1]

    def give_raise(self, percent):
        self.pay *= (1.0 + percent)

    def __str__(self):
        return ('<%s => %s: %s, %s>' %
                (self.__class__.__name__, self.name, self.job, self.pay))


class Manager(Person):
    """
    带有自定义加薪的Person
    继承了通用的 last_name, str
    """
    def __init__(self, name, age, pay):
        Person.__init__(self, name, age, pay, 'manager')

    def give_raise(self, percent, bonus=0.1):
        Person.give_raise(self, percent + bonus)

if __name__ == '__main__':
    bob = Person('Bob Smith', 44)
    sue = Person('Sue Jones', 47, 40000, 'hardware')
    tom = Manager(name='Tom Doe', age=50, pay=50000)
    print(sue, sue.pay, sue.last_name())
    for obj in (bob, sue, tom):
        obj.give_raise(.10)  # call give_raise method
        print(obj)           # call __str__ 




