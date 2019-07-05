#!/usr/bin/python

from tkinter import Label                     # 加载组件类


widget = Label(None, text='Hello GUI world!')  # 生成
widget.pack()                                   # 布置
widget.mainloop()                               # 开始事件循环
