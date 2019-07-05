"""
找到并删除命令行中指定的目录及其子目录下的所有"*.pyc"字节码文件；
假定一个不能移植的类Unix下的find命令。
"""

import os
import sys

rundir = sys.argv[1]
if sys.platform[:3] == 'win':
    findcmd = r'c:\cygwin\bin\find %s -name "*.pyc" -print' % rundir
else:
    findcmd = 'find %s -name "*.pyc" -print' % rundir

print(findcmd)
count = 0
for fileline in os.popen(findcmd):               # 在所有返回的行中迭代
    count += 1
    print(fileline, end='')
    os.remove(fileline.rstrip())                  # 行尾为\n

print('Removed %d .pyc files' % count) 