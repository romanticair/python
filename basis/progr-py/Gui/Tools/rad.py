# 以动态方式重新加载回调处理程序

from tkinter import *
import radactions                     # 首次获取回调处理程序
from importlib import reload         # 转移到Python 3.X的一个模块中


class Hello(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        Button(self, text='message1', command=self.message1).pack(side=LEFT)
        Button(self, text='message2', command=self.message2).pack(side=RIGHT)

    def message1(self):
        reload(radactions)              # 调用前需要重新加载actions模块
        radactions.message1()           # 现在单击按钮就能触发新版本

    def message2(self):
        reload(radactions)              # 调用前需要重新加载actions模块
        radactions.message2(self)       # 传递self

    def method1(self):
        print('Exposed method...')      # 从函数radactions发起调用

Hello().mainloop()