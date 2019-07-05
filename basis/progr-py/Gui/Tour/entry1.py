from tkinter import *
from quitter import Quitter


def fetch():
    print('Input => "%s"' % ent.get())

root = Tk()
ent = Entry(root)
ent.insert(0, 'Type words here')
ent.pack(side=TOP, fill=X)                                # 水平方向增大

ent.focus()                                               # 保存一个单击事件
ent.bind('<Return>', (lambda: fetch()))          # 在回车键上
btn = Button(root, text='Fecth', command=fetch)           # 在按键上
btn.pack(side=LEFT)
Quitter(root).pack(side=RIGHT)
root.mainloop()

