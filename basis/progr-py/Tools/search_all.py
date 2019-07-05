"""
####################################################################
用法："python ...\Tools\search_all.py dir string"
搜索指定的目录及其子目录下所有含有指定的字符串的文件；首先利用os.walk
接口而不是find.find来收集文件名；类似于对find.find搜索 "*" 模式的每个
返回结果调用visitfile；
####################################################################
"""

import os
import sys

listonly = False
textexts = ['.py', '.pyw', '.txt', '.c', '.h']           # 忽略二进制文件


def searchar(startdir, searchkey):
    global fcount, vcount
    fcount = vcount = 0
    for (thisDir, subsHere, filesHere) in os.walk(startdir):
        for fname in filesHere:                         # do not-dir files here
            fpath = os.path.join(thisDir, fname)         # fnames不带目录路径
            visitfile(fpath, searchkey)


def visitfile(fpath, searchkey):                       # 对于每个非目录文件进行迭代
    global fcount, vcount                               # 搜索字符串
    vcount += 1
    print(vcount, '=>', fpath)
    try:
        if not listonly:
            if os.path.splitext(fpath)[1] not in textexts:
                print('Skipping', fpath)                 # 跳过受保护的文件
            else:
                input('%s has %s' % (fpath, searchkey))
                fcount += 1
    except:
        print('Failed:', fpath, sys.exc_info()[0])

if __name__ == '__main__':
    searchar(sys.argv[1], sys.argv[2])
    print('Found in %d files, visited %d' % (fcount, vcount))

