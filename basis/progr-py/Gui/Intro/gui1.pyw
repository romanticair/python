"""
直接运行此程序，不会出现DOS控制台。
不弹出DOS控制台作为它的标准流，省了转换。
只呈现窗口，不程序脚本运行的信息。
"""
#!/usr/bin/python

from tkinter import Label                     # 加载组件类


widget = Label(None, text='Hello GUI world!')  # 生成
widget.pack()                                   # 布置
widget.mainloop()                               # 开始事件循环
