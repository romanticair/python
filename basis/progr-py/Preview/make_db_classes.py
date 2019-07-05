import shelve
from person import Person
from manager import Manager

bob = Person('Bob Smith', 44)
sue = Person('Sue Jones', 47, 40000, 'hardware')
tom = Manager('Tom Doe', 50, 50000)

db = shelve.open('class-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
db.close()

