"""创建一个简单的按钮栏，弹出对话框演示"""

from tkinter import *
from dialogTable import demos        # 按钮回调处理程序
from quitter import Quitter          # 增加一个退出对象


class Demo(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        Label(self, text='Basic demos').pack()
        for (key, value) in demos.items():
            Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)

if __name__ == '__main__':
    Demo().mainloop()


