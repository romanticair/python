class Actor:
    def line(self):
        # self.attribute will be find in subclass
        print(self.name + ": ", repr(self.says()))


class Customer(Actor):
    name = 'customer'

    def says(self):
        return "That's one ex-bird!"


class Clerk(Actor):
    name = 'Clerk'

    def says(self):
        return "no it isn't..."


class Parrot(Actor):
    name = 'parrot'

    def says(self):
        return None


class Scence:
    def __init__(self):
        self.cst = Customer()  # Embed some instance
        self.clk = Clerk()     # Scene is a composite
        self.prt = Parrot()

    def action(self):
        self.cst.line()        # Delegate to embedded
        self.clk.line()
        self.prt.line()


if __name__ == '__main__':
    a = Scence()
    a.action()
	