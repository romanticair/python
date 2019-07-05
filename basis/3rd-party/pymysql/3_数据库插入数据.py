import pymysql

db = pymysql.connect("10.0.142.171", "root", "sunck", "kaige")
cursor = db.cursor()
sql = "insert into bandcard(0, 100)"
try:
    cursor.execute(sql)
    db.commit()
except:
    # 如果提交失败，回滚到上一次数据
    db.rollback()

cursor.close()
db.close()
