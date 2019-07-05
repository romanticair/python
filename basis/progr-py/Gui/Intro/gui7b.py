import gui7
from tkinter import *


class HelloPackage(gui7.HelloPackage):
    def __getattr__(self, name):
        return getattr(self.top, name)  # 传递一个实际组件

if __name__ == '__main__':
    HelloPackage().mainloop()              # 触发__getattr__
