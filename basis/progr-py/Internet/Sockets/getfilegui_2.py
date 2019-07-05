"""
相同的，但是使用grids和import+call，而不是packs和cmdline;
直接函数调用通常比运行文件速度快；
"""

import getfile
from tkinter import *
from tkinter.messagebox import showinfo


def onSubmit():
    getfile.client(content['File'].get(), content['Port'].get(), content['Server'].get())
    showinfo('getfilegui-1', 'Download complete')

box = Tk()
labels = ['Server', 'Port', 'File']
rownum = 0
content = {}
for label in labels:
    Label(box, text=label).grid(column=0, row=rownum)
    entry = Entry(box)
    entry.grid(column=1, row=rownum, sticky=EW)
    content[label] = entry
    rownum += 1

box.columnconfigure(0, weight=0)   # make expandable
box.columnconfigure(1, weight=1)
Button(text='Submit', command=onSubmit).grid(row=rownum, column=0, columnspan=2)
box.title('getfilegui-2')
box.bind('<Return>', lambda event: onSubmit())
mainloop()
