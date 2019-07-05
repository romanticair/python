"""
直接使用Entry组件
使用固定宽度标签的行进行设置，这种方法和网格是表单设计的最好方法；
"""

from tkinter import *
from quitter import Quitter

fields = 'Name', 'Job', 'Pay'


def fetch(entries):
    for entry in entries:
        print('Input => "%s"' % entry.get())


def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=5, text=field)     # 添加标签1、输入条
        ent = Entry(row)
        row.pack(side=TOP, fill=X)                # 从顶部封装行
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)  # 从水平方向增大
        entries.append(ent)
    return entries

if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event: fetch(ents)))
    Button(root, text='Fetch', command=lambda: fetch(ents)).pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    root.mainloop()
