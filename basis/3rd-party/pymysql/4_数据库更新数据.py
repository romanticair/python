import pymysql

db = pymysql.connect("10.0.142.171", "root", "sunck", "kaige")
cursor = db.cursor()
sql = "update bandcard set money=1000 where id=1"
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

cursor.close()
db.close()
