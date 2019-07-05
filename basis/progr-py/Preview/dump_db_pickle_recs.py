import pickle
import glob

# glob 根据文件扩展名来获得该目录下所有.pkl文件
for file_name in glob.glob('*.pkl'):  # 针对 bob, sue, tom
    recfile = open(file_name, 'rb')
    record = pickle.load(recfile)
    print(file_name, '=>\n', record)

suefile = open('sue.pkl', 'rb')
print(pickle.load(suefile)['name'])  # 获取 sue 的名字