from tkinter import *

# 将默认的行为明确的显示出来，当master=None时，Tk实例默认为我们提供一个主窗口
# Toplevel组件主要用来生成新窗口(独立于主窗口)
# 请看gui1d.py，不显示调用主窗口
root = Tk()
Label(root, text='Hello GUI world!').pack(size=TOP)
root.mainloop()
