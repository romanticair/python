#!/usr/local/bin/python
"""
###############################################################################
针对具体类型，为应用提供具体的选项。
###############################################################################
"""
from shellgui import ShellGui                      # 与类型有关的gui选项
from packdlg import runPackDialog                  # 用于数据输入的对话
from unpkdlg import runUnpackDialog                # 二者都运行应用类


class TextPak1(ListMenuGui):
    def __init__(self):
        ListMenuGui.__init__(self)
        self.myMenu = [('Pack', runPackDialog),           # 简单函数
                       ('Unpack', runUnpackDialog),       # 这里使用相同的宽度
                       ('Mtool', self.notdone)]           # 来自guimixin的方法

    def forToolBar(self, label):
        return label in {'Pack', 'Unpack'}               # 3.x版本的语法


class TextPak2(DictMenuGui):
    def __init__(self):
        DictMenuGui.__init__(self)
        self.myMenu = {'Pack': runPackDialog,             # 这里也可以使用输入
                       'Unpack': runUnpackDialog,         # 输入也可不来自对话，而使用此处的
                       'Mtool': self.notdone}

if __name__ == '__main__':
    from sys import argv                                # 自测代码
    if len(argv) > 1 and argv[1] == 'list':              # 'menugui.py list|^'
        print('list test')
        TextPak1().mainloop()
    else:
        print('dict test')
        TextPak2().mainloop()
