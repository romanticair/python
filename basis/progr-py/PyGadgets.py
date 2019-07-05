"""
###################################################################################
启动多个示例程序。本程序运行时即启动这些示例程序。
本程序用于启动你最终想使用的程序。关于如何启动Python/Tk演示程序以及程序启动选项的更
多细节，请参看PyDemos。Windows下运行本程序时需注意：本程序文件是"py"文件，运行或单击
时将在控制台窗口中显示消息（其中有10秒的停顿，保持控制台可见，以便单击启动小工具）。
如要避免Windows控制台弹窗，可使用 "python.exe"（不使用"python.exe"）来运行程序，同时
将文件后缀名修改为 "pyw"，窗口属性选择“运行时最小化”，或者其他地方。
###################################################################################
"""
import sys
import time
import os
from tkinter import *
from launchmodes import PortableLauncher  # 复用程序启动类
from Gui.Tools.windows import MainWindow  # 复用窗口工具：图标、退出

mytools = [('PyEdit', 'Gui/TextEditor/textEditor.py'),
           ('PyCalc', 'Lang/Calculator/calculator.py'),
           ('PyPhoto', 'Gui/PIL/pyphoto1.py Gui/PIL/images'),
           ('PyMail', 'Internet/Email/PyMailGui/PyMailGui.py'),
           ('PyClock', 'Gui/Clock/clock.py -size 175 -bg white -picture beauti.py'),
           ('PyToe', 'Ai/TicTacToe/tictactoe.py -mode Minimax -fg white -bg navy'),
           ('PyWeb', 'LaunchBrowser.pyw -live index.html baidu.com')]
                                      # -live PyInternetDemos.html localhost:80)]
                                      # -file)]


def runImmediate(mytools):
    """
    立即启动小工具程序
    """
    print('Starting Python/Tk gadgets...')  # 消息输出到标准输出
    for (name, commandLine) in mytools:
        PortableLauncher(name, commandLine)()  # 现在调用，即刻启动
    print('One moment please...')
    if sys.platform[:3] == 'win':              # 保留控制台10秒
        for i in range(10):
            time.sleep(1)
            print('.' * 5 * (i+1))


def runLauncher(mytools):
    """
    弹出一个简单的启动器栏备用
    """
    root = MainWindow('PyGadgets Programming Python')    # 也可使用root=Tk()
    for (name, commandLine) in mytools:
        b = Button(root, text=name, fb='black', bg='beige',
                   border=2, command=PortableLauncher(name, commandLine))
        b.pack(side=LEFT, expand=YES, fill=BOTH)
    root.mainloop()

if __name__ == '__main__':
    prestart, toolbar = True, False
    if prestart:
        runImmediate(mytools)
    if toolbar:
        runLauncher(mytools)
