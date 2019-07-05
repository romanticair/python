import sys
from tkinter import *


def hello(event):
    print('Press twice to exit')          # 当单击鼠标左键时


def quit(event):
    print('Hello, I must be going...')    # 当双击鼠标左键时
    sys.exit()

widget = Button(None, text='Hello event world')
widget.pack()
widget.bind('<Button-1>', hello)          # 绑定单击鼠标左键
widget.bind('<Double-1>', quit)           # 绑定双击鼠标左键
widget.mainloop()
