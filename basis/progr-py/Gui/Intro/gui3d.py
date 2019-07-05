import sys
from tkinter import *


class HelloCallable:
    def __init__(self):                    # __init__在创建的对象上运行
        self.msg = 'Hello __call__ world'

    def __call__(self, *args, **kwargs):
        print(self.msg)                     # __call__在稍后调用时运行
        sys.exit()                          # 类对象看上去像一个函数

widget = Button(None, text='Hello event world', command=HelloCallable())
widget.pack()
widget.mainloop()
