"""
4个示例类作为独立的程序进程运行：命令行；
如果现在退出一个窗口，其它的窗口会继续存在；再这里没有简单的方法
运行所有的report调用(虽然IPC会用到套接字和管道)，
并且一些启动模式可能会丢弃程序标准输出，并且切段父类/子类
"""
from tkinter import *
from ProgrammingPython.launchmodes import PortableLauncher

demoMudules = ['demoDlg', 'demoCheck', 'demoRadio', 'demoScale']

for demo in demoMudules:
    PortableLauncher(demo, demo + '.py')  # 作为顶层程序运行

root = Tk()
root.title('Processes')
Label(root, text='Multiple program demo: command lines', bg='white').pack()
root.mainloop()
