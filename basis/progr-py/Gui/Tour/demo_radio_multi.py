# 当一些按钮具有相同值时会出现什么情况

from tkinter import *

root = Tk()
var = StringVar()
for i in range(10):
    rad = Radiobutton(root, text=str(i), variable=var, value=str(i % 3))
    rad.pack(side=LEFT)

var.set(' ')  # 首先取消全部
root.mainloop()
