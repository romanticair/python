"""
独立顶层窗口中的4个演示类；
非进程：当一个退出，其它的都会退出，因为在这里，所有的窗口都
在相同的进程中运行；在这里首先创建Tk()，不然我们会得到一个空白的默认窗口
"""
from tkinter import *

demoMudules = ['demoDlg', 'demoCheck', 'demoRadio', 'demoScale']


def makePopups(modnames):
    demoObjects = []
    for modname in modnames:
        module = __import__(modname)
        window = Toplevel()
        demo = module.Demo(window)
        window.title(module.__name__)
        demoObjects.append(demo)
    return demoObjects


def allstates(demoObjects):
    for obj in demoObjects:
        if hasattr(obj, 'report'):
            print(obj.__module__, end='')
            obj.report()

root = Tk()
root.title('Popups')
demos = makePopups(demoMudules)
Label(root, text='Multiple Toplevel window demo', bg='white').pack()
Button(root, text='States', command=lambda: allstates(demos)).pack(fill=X)
root.mainloop()
