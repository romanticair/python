from tkinter import *
from gui6 import Hello


class HelloExtender(Hello):
    def make_widgets(self):                     # 在这里拓展
        Hello.make_widgets(self)
        Button(self, text='Extend', command=self.quit).pack(side=RIGHT)

    def message(self):                           # 重新实现方法
        print('Hello', self.data)

if __name__ == '__main__':
    HelloExtender().mainloop()
