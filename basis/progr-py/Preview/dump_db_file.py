from make_db_file import load_database

# 重新将文件中载入数据库
db = load_database()
for key in db:
    print(key, '=>\n', db[key])

print(db['sue']['name'])