"""
删除目录树中所有.pyc字节码文件：如果给出命令行参数则将其作为根目录，
否则将当前工作目录作为根目录。
"""

import os
import sys

findonly = False
rootdir = sys.argv[1] if len(sys.argv) == 2 else os.getcwd()

found = removed = 0
for (thisDir, subsHere, filesHere) in os.walk(rootdir):
    for filename in filesHere:
        if filename.endswith('.pyc'):
            fullname = os.path.join(thisDir, filename)
            found += 1
            print('=>', fullname)
            if not findonly:
                try:
                    os.remove(fullname)
                    removed += 1
                except:
                    etype, inst = sys.exc_info()[:2]
                    print('*' * 4, 'Failed', filename, etype, inst)

print('Found', found, 'files, removed', removed)

