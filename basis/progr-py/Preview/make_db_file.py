"""
用自定义格式将内存数据库对象保存在文件中；
假定数据不使用'endrec.', 'endb.'和'=>'；
假定数据库是字典的字典；
警告：使用 eval 可能存在危险，它会将字符串当做代码执行；
也可以使用 eval() 一次创建一条字典记录；
对于print(key, file=dbfile)，也可以使用dbfile.write(key + '\n')
"""

db_file_name = 'people-file'
ENDDB = 'enddb.'
ENDREC = 'endrec.'
RECSEP = '=>'


def store_database(db, file_name=db_file_name):
    """将数据库格式化保存为普通文件"""
    db_file = open(file_name, "w")
    for key1 in db:
        print(key1, file=db_file)
        for (key2, value) in db[key1].items():
            print(key2 + RECSEP + repr(value), file=db_file)
        print(ENDREC, file=db_file)

    print(ENDDB, file=db_file)
    db_file.close()


def load_database(file_name=db_file_name):
    """解析数据，重新构建数据库"""
    db_file = open(file_name)
    import sys
    sys.stdin = db_file
    db = {}
    key = input()
    while key != ENDDB:
        rec = {}
        field = input()
        while field != ENDREC:
            name, value = field.split(RECSEP)
            rec[name] = eval(value)
            field = input()
        db[key] = rec
        key = input()

    return db


if __name__ == '__main__':
    from initdata import db
    store_database(db)












