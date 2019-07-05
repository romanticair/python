# interactive query

import shelve

field_names = ('name', 'age', 'job', 'pay')
max_field = max(len(f) for f in field_names)
db = shelve.open('class-shelve')
while True:
    key = input('\nKey? => ')  # 键或空行，空行退出
    if not key:
        db.close()
        break
    try:
        record = db[key]       # 一句键获取记录，在控制台显示
    except KeyError:
        print('No such key "%s"!' % key)
    else:
        for field in field_names:
            # 以最长字段名左对齐
            print(field.ljust(max_field), '=>', getattr(record, field))

