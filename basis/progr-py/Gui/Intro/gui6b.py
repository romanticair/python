from sys import exit
from tkinter import *
from gui6 import Hello

parent = Frame(None)           # 生成一个容器组件
parent.pack()
Hello(parent).pack(side=RIGHT)  # 附加Hello，而不运行
Button(parent, text='Attach', command=exit).pack(side=LEFT)
parent.mainloop()
