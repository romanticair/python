# interactive update

import shelve
from person import Person

field_names = ('name', 'age', 'job', 'pay')
db = shelve.open('class-shelve')
while True:
    key = input('\nKey? => ')
    if not key:
        break
    if key in db:
        record = db[key]  # 更新存在的记录
    else:
        record = Person(name='?', age='?')  # 或者创建/保存新的记录
    for field in field_names:
        current_value = getattr(record, field)
        new_text = input('\t[%s]=%s\n\t\tnew?=>' % (field, current_value))
        if new_text:
            setattr(record, field, eval(new_text))
    db[key] = record

db.close()