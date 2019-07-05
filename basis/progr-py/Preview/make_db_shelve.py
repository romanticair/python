import shelve
from initdata import bob, sue

db = shelve.open('people-shelve')  # 会生成*.bak, *.dat, *.dir文件
db['bob'] = bob
db['sue'] = sue
db.close()
