# 对数据库进行一些修改，载入文件、更新和重新保存

from make_db_file import load_database, store_database

db = load_database()
db['sue']['pay'] *= 1.10
db['tom']['name'] = 'Tom Tom'

store_database(db)