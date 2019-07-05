# 以递归的方式列举目录树中的文件

import sys
import os


def mylister(currdir):
    print('[' + currdir + ']')
    for file in os.listdir(currdir):       # 列举文件
        path = os.path.join(currdir, file)  # 把目录路径添加回去
        if not os.path.isdir(path):
            print(path)
        else:
            mylister(path)                  # 递归进入子目录


if __name__ == '__main__':
    mylister(sys.argv[1])