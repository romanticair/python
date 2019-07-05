"""
找出单个目录下最大的Python源代码文件。
搜索Windows Python源代码库，除非指定了dir命令行参数。
"""

import sys
import glob
import os

dirname = r'L:\Python\Lib' if len(sys.argv) == 1 else sys.argv[1]

allsizes = []
apply = glob.glob(dirname + os.sep + '*.py')
for filename in apply:
    filesize = os.path.getsize(filename)
    allsizes.append((filesize, filename))

allsizes.sort()
print(allsizes[:2])   # the minimum
print(allsizes[-2:])  # the maximum