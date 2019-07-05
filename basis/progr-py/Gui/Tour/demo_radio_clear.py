# 好好利用你的单选按钮变量（这确实是难以理解的东西）

from tkinter import *

root = Tk()


def radio1():
    # global tmp                        # 局部变量是暂时的
    tmp = IntVar()                      # 变为全局变量可以解决问题
    for i in range(10):
        rad = Radiobutton(root, text=str(i), value=str(i), variable=tmp)
        rad.pack(side=LEFT)
    tmp.set(5)                          # 选第六个按钮

radio1()
root.mainloop()