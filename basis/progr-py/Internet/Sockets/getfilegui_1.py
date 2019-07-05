"""
从简单的Tkinter GUI上启动getfile脚本客户端；
也可以使用os.fork+exec, os.spawnv(参加Launcher);
windows: 如果在路径上没有，用'start'代替'python'；
"""
import os
import sys
from tkinter import *
from tkinter.messagebox import showinfo


def onReturnKey():
    cmdline = ('python getfile.py -mode client -file %s -port %s -host %s' %
               content['File'].get(), content['Port'].get(), content['Server'].get())
    os.system(cmdline)
    showinfo('getfilegui_1', 'Download complete')

box = Tk()
labels = ['Server', 'Port', 'File']
content = {}
for label in labels:
    row = Frame(box)
    row.pack(fill=X)
    Label(row, text=label, width=6).pack(side=LEFT)
    entry = Entry(row)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    content[label] = entry

box.title('getfilegui-1')
box.bind('<Return>', lambda event: onReturnKey())
mainloop()
