# 单选按钮，简单的方法

from tkinter import *

root = Tk()
var = IntVar(0)  # 选择0来开始
for i in range(10):
    rad = Radiobutton(root, text=str(i), value=str(i), variable=var)
    rad.pack(side=LEFT)

root.mainloop()
print(var.get())
