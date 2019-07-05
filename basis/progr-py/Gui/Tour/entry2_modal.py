# 设置表单对话框为模态，必须在销毁前通过输入取回

from tkinter import *
from entry2 import makeform, fetch, fields


def show(entries, popup):
    fetch(entries)                          # 必须在销毁前取回
    popup.destroy()                         # 如果修改了stmt order, msgshi随之失败


def ask():
    popup = Toplevel()                      # 在模态对话框窗口中显示表单
    ents = makeform(popup, fields)
    Button(popup, text='OK', command=(lambda: show(ents, popup))).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()                     # 在这里等待销毁

root = Tk()
Button(root, text='Dialog', command=ask).pack()
root.mainloop()
