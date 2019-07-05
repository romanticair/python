import sys
from tkinter import *


class HelloClass:
    def __init__(self):
        widget = Button(None, text='Hello event world', command=self.quit)
        widget.pack()

    def quit(self):
        print('Hello class method world')  # self.quit是一个bound方法
        sys.exit()                         # 保留住self+quit对

HelloClass()
mainloop()

