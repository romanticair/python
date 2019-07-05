from MySql import SunckSql

s = SunckSql("10.0.142.171", "root", "sunck", "kaige")
res = s.get_all("select * from bandcard where money>400")
for row in res:
    print("%d - - %d" % (row[0], row[1]))
