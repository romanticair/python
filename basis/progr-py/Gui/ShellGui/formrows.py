"""
创建一个"标签+数据项"的行式文本框，带有可选的文件打开、浏览按钮；
这是一个独立的模块，其代码可部分存在于其他程序中；当选中某行时，
调用方保留返回的、与当前行有关联的var变量；
"""
from tkinter import *
from tkinter.filedialog import askopenfilename


def makeFormRow(parent, label, width=15, browse=True, extend=False):
    var = StringVar()
    row = Frame(parent)
    lab = Label(row, text=label + '?', relief=RIDGE, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)
    lab.pack(side=LEFT)                                           # 使用打包的行式图文框
    ent.pack(side=LEFT, expand=YES, fill=X)                       # 使用固定宽度的标签或者网格(row, col)
    if browse:
        btn = Button(row, text='browser...')
        btn.pack(side=RIGHT)
        if not extend:
            btn.config(command=lambda: var.set(askopenfilename() or var.get()))
        else:
            btn.config(command=lambda: var.set(var.get() + ' ' + askopenfilename()))
    return var
