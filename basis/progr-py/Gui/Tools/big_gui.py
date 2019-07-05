"""
GUI 实现演示，结合了maker、mixin和this。
"""
import sys, os
from tkinter import *
from Gui.Tools.guimixin import *            # mix-in中的方法，包括quit, spawn等
from Gui.Tools.guimaker import *            # 框架、菜单、工具栏生成器


class Hello(GuiMixin, GuiMakerWindowMenu):  # 或者GuiMakerFrameMenu
    def start(self):
        self.hellos = 0
        self.master.title('GuiMaker Demo')
        self.master.iconname('GuiMaker')
        def spawnme():
            self.spawn('big_gui.py')                                      # 对比：推迟调用和lambda表达式

        self.menuBar = [                                                  # 一棵树，有3个下拉菜单
            ('File', 0, [('New...', 0, spawnme),                          # 下拉菜单
                         ('Open...', 0, self.fileOpen),                   # 菜单下的项目列表
                         ('Quit', 0, self.quit)]),                        # 菜单下的标签，加下划线操作
            ('Edit', 0, [('Cut', -1, self.notdone),                       # 不加下划线，操作
                         ('Paste', -1, self.notdone),                     # lambda: 0也有效果
                         'separator',                                     # 添加分割线
                         ('Stuff', -1, [('Clone', -1, self.clone),        # 级联式子菜单
                                        ('More', -1, self.more)]),
                         ('Delete', -1, lambda: 0),
                         [5]]),                                           # 禁用 "Delete" 项
            ('Play', 0, [('Hello', 0, self.greeting),
                         ('Popup...', 0, self.dialog),
                         ('Demos', 0, [('Toplevels', 0, lambda: self.spawn(r'..\Tour\toplevel2.py')),
                                       ('Frames', 0, lambda: self.spawn(r'..\Tour\demoAll_frm_ridge.py')),
                                       ('Images', 0, lambda: self.spawn(r'..\Tour\buttonpics.py')),
                                       ('Alarm', 0, lambda: self.spawn(r'..\Tour\alarm.py', wait=False)),
                                       ('Other...', -1, self.pickDemo)]
                          )],
             )]
        self.toolBar = [('Quit', self.quit, dict(side=RIGHT)),            # 添加3个按钮
                        ('Hello', self.greeting, dict(side=LEFT)),        # 也可使用{'side': RIGHT}
                        ('Popup', self.dialog, dict(side=LEFT, expand=YES))]

    def makeWidgets(self):
        middle = Label(self, text='Hello maker world!', width=40, height=10,
                       relief=SUNKEN, cursor='pencil', bg='white')        # 重写默认值，窗口中部
        middle.pack(expand=YES, fill=BOTH)

    def greeting(self):
        self.hellos += 1
        if self.hellos % 3:
            print('hi')
        else:
            self.infobox('Three', 'HELLO!')                               # 每按3次按钮

    def dialog(self):                                                    # 经典风格，忽略多个参数
        button = self.question('OOPS!', 'You typed "rm*" ... continues?', 'questhead', ('yes', 'no'))
        [lambda: None, self.quit][button]()                             # [False]return None else self.quit

    def fileOpen(self):
        pick = self.selectOpenFile(file='big_gui.py')
        if pick:
            self.browser(pick)                                            # 浏览自己的源文件，或其它文件

    def more(self):
        new = Toplevel()
        Label(new, text='A new non-modal window').pack()
        Button(new, text='Quit', command=self.quit).pack(side=LEFT)
        Button(new, text='More', command=self.more).pack(side=RIGHT)

    def pickDemo(self):
        pick = self.selectOpenFile(dir='..')
        if pick:
            self.spawn(pick)                                              # 生成任意Python程序

if __name__ == '__main__':
    Hello().mainloop()                                                    # 构建一个，运行一个
