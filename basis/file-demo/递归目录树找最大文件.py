# Find the largest Python source file in an entire directory tree

import sys, os, pprint


if sys.platform[:3] == 'win':
    dirname = r'L:\python\lib'
else:
    dirname = '/usr/lib/python'

allsize = []
for (thisDir, subsHere, filesHere) in os.walk(dirname):
    for filename in filesHere:
        if filename.endswith('.py'):
            fullname = os.path.join(thisDir, filename)
            fullsize = os.path.getsize(fullname)
            allsize.append((fullsize, fullname))

allsize.sort()
pprint.pprint(allsize[:2])
pprint.pprint(allsize[-2:])
