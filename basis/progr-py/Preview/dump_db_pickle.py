import pickle

db_file = open('people-pickle', 'rb')  # 二进制模式文件
db = pickle.load(db_file)
for key in db:
    print(key, '=>\n', db[key])

print(db['sue']['name'])
