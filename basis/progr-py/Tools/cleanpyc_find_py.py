"""
找到并删除命令行中指定的目录及其子目录下的所有"*.pyc"字节码文件；
它使用了一个Python编码的寻找工具，因此是可跨平台移植的；可运行此
脚本删除老的Python版本留下的.pyc文件；
"""
import os
import sys
import find

count = 0
for filename in find.find('*.pyc', sys.argv[1]):
    count += 1
    print(filename)
    os.remove(filename)

print('Removed %d .pyc files' % count) 