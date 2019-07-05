from person import Person

class Manager(Person):
    def give_raise(self, percent, bonus=0.1):
        self.pay *= (1.0 + bonus + percent)
        # Person.give_raise(self, bonus + bonus) will be better

if __name__ == '__main__':
    tom = Manager(name='Tom Doe', age=50, pay=50000)
    print(tom.last_name())
    tom.give_raise(.20)
    print(tom.pay)

