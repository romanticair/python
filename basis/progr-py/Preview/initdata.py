# 初始化将存储于文件、pickle和shelve的数据

# 记录
bob = {'name': 'Bob', 'age': 42, 'pay': 30000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 45, 'pay': 40000, 'job': 'hdw'}
tom = {'name': 'Tom', 'age': 50, 'pay': 0, 'job': None}

# 数据库
db = dict()
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom


if __name__ == '__main__':
    for key in db:
        print(key, '=>\n', db[key])
