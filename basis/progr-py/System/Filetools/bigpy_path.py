"""
找出模块导入搜索路径下最大的Python源代码。跳过已访问过的目录，
同一路径和大小写的格式以便使之正确匹配，并在pprint打印结果中添加
文件行数。使用os.environ['PYHTHONPATH']并不够，它只是sys.path的一个子集。
"""

# 我的系统的字段不是'PYHTHONPATH'.

import sys
import os
import pprint
import time

# 1代表目录，2代表加上文件
TRACE = 0

start = time.time()
visited = {}
allsizes = []
for scrdir in sys.path:
    for (thisDir, subsHere, filesHere) in os.walk(scrdir):
        if TRACE > 0:
            print('...', thisDir)
        thisDir = os.path.normpath(thisDir)
        fixcase = os.path.normcase(thisDir)
        if fixcase in visited:
            continue
        else:
            visited[fixcase] = True
        for filename in filesHere:
            if filename.endswith('.py'):
                if TRACE > 1:
                    print('...', filename)
                pypath = os.path.join(fixcase, filename)
                try:
                    pysize = os.path.getsize(pypath)
                except os.error:
                    print('skipping', pypath, sys.exc_info()[0])
                else:
                    pylines = len(open(pypath, 'rb').readlines())
                    allsizes.append((pysize, pylines, pypath))

print('By size....')
allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])

print('By lines...')
allsizes.sort(key=lambda x: x[1])
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])
end = time.time()

print('It used ', end - start)