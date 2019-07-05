"""
用法："python ..\Tools\visitor_replace.py rootdir fromStr toStr"。在目录树里的
所有文件中进行搜索并替换：在所有文本文件中将fromStr替换成toStr：这个工具强大而
危险！！visitor_edit.py运行一个编辑器，以供你验证改动并进行编辑，因此相对安全一些；
可以使用visitor_collect.py来仅仅收集匹配文件名单；这里的listonly模式与SearchVisitor
和CollectVisitor类似；
"""

import sys
from visitor import SearchVisitor


class ReplaceVisitor(SearchVisitor):
    """
    将startDir及其子目录下所有文件中的fromStr替换成toStr；运行后，修改过变量的
    文件存储在列表obj.changed中；
    """
    def __init__(self, fromStr, toStr, listOnly=False, trace=0):
        self.changed = []
        self.toStr = toStr
        self.listOnly = listOnly
        super(ReplaceVisitor, self).__init__(fromStr, trace)
        # SearchVisitor.__init__(self, fromStr, trace)

    def visitmatch(self, fname, text):
        self.changed.append(fname)
        if not self.listOnly:
            fromStr, toStr = self.context, self.toStr
            text = text.replace(fromStr, toStr)         # 可能需要使用字节
            open(fname, 'w').write(text)                # 'w' -> 'wb' ?

if __name__ == '__main__':
    listonly = input('List only?') == 'y'
    visitor = ReplaceVisitor(sys.argv[2], sys.argv[3], listonly)
    if listonly or input('Proceed with changes?') == 'y':
        visitor.run(startDir=sys.argv[1])
        action = 'Changed' if not listonly else 'Found'
        print('Visited %d files' % visitor.fcount)
        print(action, '%d files:' % len(visitor.changed))
        for fname in visitor.changed:
            print(fname)