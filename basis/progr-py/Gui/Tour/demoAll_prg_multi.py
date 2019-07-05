"""
4个示例类作为独立的程序进程运行；multiprocessing；
multiprocessing允许我们使用参数启动已命名的函数，
但不包括lambda表达式，因为它们在Windows上不能pickle的；
multiprocessing也有其自己的IPC工具，如用于通信的管道；
"""

from tkinter import *
from multiprocessing import Process

demoMudules = ['demoDlg', 'demoCheck', 'demoRadio', 'demoScale']


def runDemo(modname):              # 新进程进行
    module = __import__(modname)
    module.Demo().mainloop()

if __name__ == '__main__':
    for modname in demoMudules:
        Process(target=runDemo, args=(modname,)).start()

    root = Tk()                      # 父类线程GUI
    root.title('Processes')
    Label(root, text='Multiple program demo: multiprocessing', bg='white').pack()
    root.mainloop()
