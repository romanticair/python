import shelve

db = shelve.open('class-shelve')
sue = db['sue']
sue.give_raise(.25)
db['sue'] = sue

tom = db['tom']
tom.give_raise(.20)
db['tom'] = tom

db.close()
