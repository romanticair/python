"""
一个窗口上的4个演示类组件（子框架）；
这一个窗口上有5个Quitter按钮，每个按钮都能终止整个GUI；
在容器、独立窗口或进程中，GUI能够作为框架重复使用；
"""

from tkinter import *
from quitter import Quitter

demoMudules = ['demoDlg', 'demoCheck', 'demoRadio', 'demoScale']
parts = []


def addComponents(root):
    for demo in demoMudules:
        module = __import__(demo)               # 通过名称字符串导入，也可以exec或者eval
        part = module.Demo(root)                # 附加一个示例
        part.config(bd=2, relief=GROOVE)        # 像Demo()传递配置
        part.pack(side=LEFT, expand=YES, fill=BOTH)
        parts.append(part)


def dumpState():
    for part in parts:
        print(part.__module__ + ':', end=' ')
        if hasattr(part, 'report'):
            part.report()
        else:
            print('None')

root = Tk()
root.title('Frames')
Label(root, text='Multiple Frame demo', bg='white').pack()
Button(root, text='States', command=dumpState).pack(fill=X)
Quitter(root).pack(fill=X)
addComponents(root)
root.mainloop()
