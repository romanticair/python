# 图形用户界面读取器：类似于pipes_gui1程序，但使根窗口和主循环显示呈现。

from tkinter import *
from Gui.Tools.guiStreams import redirectedGuiShellCmd


def launch():
    redirectedGuiShellCmd('python -u pipe_nongui.py')

win = Tk()
Button(win, text='Go!', command=launch).pack()
win.mainloop()
