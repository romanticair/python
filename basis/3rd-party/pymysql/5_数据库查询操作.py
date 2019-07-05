"""
fetchone()
功能：获取下一个查询结果集，结果集是一个对象

fetchall()
功能：接受全部的返回的行

rowcount:是一个只读数据, 返回execute()执行返回的数据

"""
import pymysql

db = pymysql.connect("10.0.142.171", "root", "sunck", "kaige")
cursor = db.cursor()
sql = "select * from bandcard where money>400"
try:
    cursor.execute(sql)
    reslist = cursor.fetchall()
    for row in reslist:
        print("%d - - %d" % (row[0], row[1]))

except:
    cursor.rock()

cursor.close()
db.close()