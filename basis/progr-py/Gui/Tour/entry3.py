"""
使用StringVar变量
通过列进行布局：这可能造成所有位置都不能水平对齐
"""

from tkinter import *
from quitter import Quitter

fields = 'Name', 'Job', 'Pay'


def fetch(variables):
    for variable in variables:
        print('Input => "%s"' % variable.get())  # 从变量充获得


def makeform(root, fields):
    form = Frame(root)
    left = Frame(form)
    right = Frame(form)
    form.pack(fill=X)
    left.pack(side=LEFT)
    right.pack(side=RIGHT, expand=YES, fill=X)

    variables = []
    for field in fields:
        lab = Label(left, width=5, text=field)
        ent = Entry(right)
        lab.pack(side=TOP)
        ent.pack(side=TOP, fill=X)
        var = StringVar()
        ent.config(textvariable=var)
        var.set('enter here')
        variables.append(var)
    return variables

if __name__ == '__main__':
    root = Tk()
    vars = makeform(root, fields)
    Button(root, text='fetch', command=(lambda: fetch(vars))).pack(side=LEFT)
    Quitter(root).pack(side=LEFT)
    root.bind('<Return>', (lambda event: fetch(vars)))
    root.mainloop()
    
