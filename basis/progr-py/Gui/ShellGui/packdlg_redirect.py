# 将命令行脚本包装到图形界面重定向工具中，输出显示到弹出式窗口中

from tkinter import *
from packdlg import runPackDialog
from Gui.Tools.guiStreams import redirectedGuiFunc


def runPackDialog_Wrapped():          # 在mytools.py中运行的回调函数
    redirectedGuiFunc(runPackDialog)  # 对整个回调处理程序进行包装
	
if __name__ == '__main__':
    root = Tk()
	Button(root, text='pop', command=runPackDialog_Wrapped).pack(fill=X)
	root.mainloop()
