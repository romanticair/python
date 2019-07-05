from initdata import db
import pickle

db_file = open('people-pickle', 'wb')  # 二进制模式文件
pickle.dump(db, db_file)  # 字节数据，非字符串
db_file.close()

