"""
用法：""python ...\Tools\visitor_cpall.py fromDir toDir trace?
类似System\Filetools\cpall.py，不过借助visitor类和os.walk；在传入
遍历器的所有命令前将fromDir替换成toDir；假定toDir一开始不存在；
"""
import os
from visitor import FileVisitor                                  # 访问器在'.'目录下
from System.Filetools.cpall import copyfile                      # 在路径中是一个目录


class CpallVisitor(FileVisitor):
    def __init__(self, fromDir, toDir, trace=True):
        self.fromDirLen = len(fromDir) + 1
        self.toDir = toDir
        FileVisitor.__init__(self, trace=trace)

    def visitdir(self, dirpath):
        toPath = os.path.join(self.toDir, dirpath[self.fromDirLen:])
        if self.trace:
            print('d', dirpath, '=>', toPath)
        os.mkdir(toPath)
        self.dcount += 1

    def visitfile(self, filepath):
        toPath = os.path.join(self.toDir, filepath[self.fromDirLen:])
        if self.trace:
            print('f', filepath, '=>', toPath)
        copyfile(filepath, toPath)
        self.fcount += 1

if __name__ == '__main__':
    import sys
    import time
    fromDir, toDir = sys.argv[1:3]
    trace = len(sys.argv) > 3
    print('Copying...')
    start = time.clock()
    walker = CpallVisitor(fromDir, toDir, trace)
    walker.run(startDir=fromDir)
    print('Copied', walker.fcount, 'files', walker.dcount, 'directories', end=' ')
    print('in', time.clock() - start, 'seconds') 