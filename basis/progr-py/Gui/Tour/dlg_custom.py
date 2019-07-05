import sys
from tkinter import *

makemodal = (len(sys.argv) > 1)


def dialog():
    win = Toplevel()                                     # 创建新窗口
    Label(win, text='Hard drive reformatted!').pack()    # 增加一些组件
    Button(win, text='Ok', command=win.destroy).pack()   # 设置销毁回调
    if makemodal:                                        # 如果为模态
        win.focus_set()                                  # 获得输入焦点
        win.grab_set()                                   # 在打开的时候，禁用其它窗口
        win.wait_window()                                # 在win销毁前，继续等待
    print('dialog exit')                                 # 否则，立即返回

root = Tk()
Button(root, text='popup', command=dialog).pack()
root.mainloop()

