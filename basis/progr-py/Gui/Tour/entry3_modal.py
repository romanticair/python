# 能够在销毁后使用StringVar获取值

from tkinter import *
from entry3 import makeform, fetch, fields


def show(variables, popup):
    popup.destroy()          # 顺序在这里无关紧要
    fetch(variables)         # 变量在窗口摧毁后仍存在


def ask():
    popop = Toplevel()
    vars = makeform(popop, fields)
    Button(popop, text='Ok', command=(lambda: show(vars, popop))).pack()
    popop.grab_set()
    popop.focus_set()
    popop.wait_window()      # 在这里等待摧毁

root = Tk()
Button(root, text='Dialog', command=ask).pack()
root.mainloop()


