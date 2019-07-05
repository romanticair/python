"""
##################################################################################
测试："python ...\Tools\visitor.py dir testmask [string]"。使用类和子类分装
os.walk调用手法某些细节，一遍进行遍历和搜索；testmask是一个整数比特掩码，每个
可用的自我测试占1位；另请参照：visitor_*/.py子类用例；框架中一般应当使用__X作为
伪局部名称，不过位了在子类和客户端的使用，这里的所有名称都将到处；可重新定义reset
以支持多个需要更新子类的相互独立的遍历操作；
##################################################################################
"""

import os
import sys


class FileVisitor:
    """
    访问startDir(默认为'.')下所有非目录文件；可通过重载visit*方法定制
    文件/目录处理器；情境参数/属性为可选的子类特异的状态；追踪开关：
    0代表关闭，1代表显示目录，2代表显示目录及文件
    """
    def __init__(self, context=None, trace=2):
        self.fcount = 0
        self.dcount = 0
        self.context = context
        self.trace = trace

    def run(self, startDir=os.curdir, reset=True):
        if reset:
            self.reset()
        for (thisDir, subsHere, filesHere) in os.walk(startDir):
            self.visitdir(thisDir)
            for fname in filesHere:                     # 对非目录文件进行迭代
                fpath = os.path.join(thisDir, fname)     # fname不带路径
                self.visitfile(fpath)

    def reset(self):                                    # 为了重复使用遍历器
        self.fcount = self.dcount = 0                    # 为了相互独立的遍历操作

    def visitdir(self, dirpath):                       # call for each dir
        self.dcount += 1                                 # 带重写或扩展
        if self.trace > 0:
            print(dirpath, '...')

    def visitfile(self, filepath):                     # call for each file
        self.fcount += 1                                 # 带重写或扩展
        if self.trace > 0:
            print(self.fcount, '=>', filepath)


class SearchVisitor(FileVisitor):
    """
    在startDir及其目录下的文件中搜索字符串；子类：根据需要重新定义
    visitmatch、扩展列表和候选；子类可以使用testexts来指定进行搜索的文件
    类型（还可以重新定义候选以对文本内容使用mimetypes: 参考之前相关部分）。
    """
    skipexts = []
    testexts = ['.txt', '.pyw', '.py', '.html', '.c', '.h']  # 搜索带有这些扩展名的文件
    # skipexts = ['.gif', '.jpg', '.pyc', '.o', '.a', '.exe']# 或者跳过带有这些扩展的文件

    def __init__(self, searchkey, trace=2):
        FileVisitor.__init__(self, searchkey, trace)
        self.scount = 0

    def reset(self):                                    # 进行互相独立的遍历时
        self.scount = 0

    def candidate(self, fname):                        # 重写定义mimetypes
        ext = os.path.splitext(fname)[1]
        if self.testexts:                                # 在测试列表中
            return ext in self.testexts
        else:                                            # 或者不在跳过列表中
            return ext not in self.skipexts

    def visitfile(self, fname):                         # 匹配测试
        FileVisitor.visitfile(self, fname)
        if not self.candidate(fname):
            if self.trace > 0:
                print('Skipping', fname)
        else:
            text = open(fname, 'rb').read()               # 如果不能解码则使用'rb'模式
            if self.context.encode() in text:            # 也可以使用text.find() != -1
                self.visitmatch(fname, text)              # 在这里作比较，我用了字节比较
                self.scount += 1

    def visitmatch(self, fname, text):                  # 处理一个匹配文件
        print('%s has %s' % (fname, self.context))        # 在低一级的水平重写

if __name__ == '__main__':                                # 自测逻辑业务
    dolist = 1
    dosearch = 2                                          # 3=进行列出和搜索
    donext = 4                                            # 添加了下一个测试时

    def selftest(testmask):
        if testmask & dolist:
            visitor = FileVisitor(trace=2)
            visitor.run(sys.argv[2])
            print('Visited %d files and %d dirs' % (visitor.fcount, visitor.dcount))
        if testmask & dosearch:
            visitor = SearchVisitor(sys.argv[3], trace=0)
            visitor.run(sys.argv[2])
            print('Found in %d files, visited %d' % (visitor.scount, visitor.fcount))

    selftest(int(sys.argv[1]))                            # 例如：3 = dolist | dosearch
