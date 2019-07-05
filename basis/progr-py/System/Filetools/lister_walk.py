"""用os.walk完成目录树列举"""

import sys
import os


def lister(root):
    for (thisdir, subshere, fileshere) in os.walk(root):  # 生成目录树的目录列表
        print('[' + thisdir + ']')
        for fname in fileshere:                           # 打印该目录下的文件
            path = os.path.join(thisdir, fname)            # 添加目录名前缀
            print(path)

if __name__ == '__main__':
    lister(sys.argv[1])                                    # 从命令行传入目录名 