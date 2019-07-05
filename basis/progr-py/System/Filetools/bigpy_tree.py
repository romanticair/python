"""
找出整个目录树中最大的Python源代码文件。
搜索Python源代码库，利用pprint漂亮地显示结果。
"""

import os
import pprint
import sys

TRACE = False


if sys.platform.startswith('win'):
    dirname = r'L:\Python\Lib'   # Windows
else:
    dirname = '/usr/lib/python'  # Unix, Linux, Cygwin

allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(dirname):
    if TRACE:
        print(thisDir)
    for filename in filesHere:
        if filename.endswith('.py'):
            if TRACE:
                print('...', filename)
            fullname = os.path.join(thisDir, filename)
            fullsize = os.path.getsize(fullname)
            allsizes.append((fullsize, fullname))

allsizes.sort()
pprint.pprint(allsizes[:2])
pprint.pprint(allsizes[-2:])
