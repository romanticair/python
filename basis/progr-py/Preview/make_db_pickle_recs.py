# 存储数据库中的一一条记录到一个普通文件的方式改进

from initdata import bob, sue, tom
import pickle

for (key, record) in [('bob', bob), ('tom', tom), ('sue', sue)]:
    recfile = open(key + '.pkl', 'wb')
    pickle.dump(record, recfile)
    recfile.close()


