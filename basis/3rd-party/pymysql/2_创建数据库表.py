import pymysql

db = pymysql.connect("10.0.142.171", "root", "sunck", "kaige")
cursor = db.cursor()

# 检查表是否存在，若存在则删除
cursor.execute("drop table if exists bandcard")
# 建表
sql = "create table bandcard(id int auto_increament primary key,"\
      "money int not null)"
cursor.execute(sql)

cursor.close()
db.close()


