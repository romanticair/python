import pymysql

# 链接数据库
# 参数1: mysql服务所在的主机IP
# 参数2: 用户名
# 参数3: 密码
# 参数4: 要链接的数据库名
db = pymysql.connect("localhost", "root", "sunck", "kaige")
# 创建一个cursor对象
cursor = db.cursor()
sql  = "select version()"
# 执行语句
cursor.execute(sql)
# 获取返回的信息
data = cursor.fetclone()
print(data)
# 断开
cursor.close()
db.close()
