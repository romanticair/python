#!/usr/bin/python
"""
###############################################################
返回某个根目录及其子目录下所有匹配某个文件名模式的文件；
使用os.walk循环，不支持修建子目录，并且可作为顶层脚本运行；

find()是一个生成器，利用os.walk()生成器产生匹配的文件名，可使用
findlist()强制生成结果列表；
###############################################################
"""

import fnmatch
import os


def find(pattern, startdir=os.curdir):
    for (thisDir, subsHere, filesHere) in os.walk(startdir):
        for name in subsHere + filesHere:         # 遍历子目录列表和文件列表
            if fnmatch.fnmatch(name, pattern):
                fullpath = os.path.join(thisDir, name)
                yield fullpath


def findlist(pattern, startfir=os.curdir, dosort=False):
    matches = list(find(pattern, startfir))
    if dosort:
        matches.sort()
    return matches

if __name__ == '__main__':
    import sys
    namepattern, startdir = sys.argv[1], sys.argv[2]
    for name in find(namepattern, startdir):
        print(name) 

















