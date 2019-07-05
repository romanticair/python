# Find the largest Python source file in a single directory

import os, glob
# dirname = r'L:\python\lib'
dirname = os.getcwd()  # I test the current directory


allsizes = []
allpy = glob.glob(dirname + os.sep + '*.py')
for filename in allpy:
    filesize = os.path.getsize(filename)
    allsizes.append((filename, filesize))

allsizes.sort()
print('The smallest: ', allsizes[:2])
print('The largest: ', allsizes[-2:]) 