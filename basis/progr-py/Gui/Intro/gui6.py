from tkinter import *


class Hello(Frame):                     # 一个扩展框架
    def __init__(self, parent=None):
        Frame.__init__(self, parent)      # 子类初始化
        self.pack()
        self.data = 42
        self.make_widgets()               # 将组建附加到self

    def make_widgets(self):
        widget = Button(self, text='Hello frame world!', command=self.message)
        widget.pack(side=LEFT)

    def message(self):
        self.data += 1
        print('Hello frame world %d!' % self.data)

if __name__ == '__main__':
    Hello.mainloop()
