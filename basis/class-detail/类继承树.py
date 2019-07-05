class Animal:
    def speak(self):
        print('I\'m a Animal')

    def reply(self):
        self.speak()  # Back to subclass


class Mammal(Animal):
    def speak(self):
        print('This is the kind of  Mammal Animal')


class Cat(Mammal):
    def speak(self):
        print('Cat Cat')


class Dog(Mammal):
    def speak(self):
        print('Dog Dog')


class Primate(Mammal):
    def speak(self):
        print('Primate Primate')


class Hacker(Primate):
    pass  # Inherit from Primate


if __name__ == '__main__':
    spot = Cat()
    spot.reply()
    data = Hacker()
    data.reply()
