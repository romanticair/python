"""
用法："python ..\Tools\visitor_edit.py string rootdir?"。
对SearchVisitor添加一个作为外部子类组分的编辑器自动启动行为；在遍历过程中
对含有字符串的每个文件自动弹出一个编辑器；在Windows下海可以使用editor='edit'
或'notepad'；后面的GUI编程，可试试r'python Gui\TextEditor\textEditor.py'；
也可以传入一些搜索命令，在某些编辑器启动时即跳到第一处匹配；
"""

import os
import sys
from visitor import SearchVisitor


class EditVisitor(SearchVisitor):
    """
    编辑startDir及其子目录下含有字符串的文件
    """
    editor = r'L:\Notepad++\notepad++.exe'                 # 请根据你的计算机上的编辑器来定位

    def visitmatch(self, fpathname, text):
        os.system('%s %s' % (self.editor, fpathname))

if __name__ == '__main__':
    visitor = EditVisitor(sys.argv[1])
    visitor.run('.' if len(sys.argv) < 3 else sys.argv[2])
    print('Edited %d files, visited %d' % (visitor.scount, visitor.fcount)) 