from tkinter import *


def dialog():
    win = Toplevel()
    Label(win, text='Hard drive reformatted!').pack()
    Button(win, text='OK', command=win.quit).pack()   # 设置退出回调
    win.protocol('WM_DELETE_WINDOW', win.quit)        # 在wm关闭时退出！

    win.focus_set()                                   # 奇怪的退出
    win.grab_set()  # 在打开的时候禁用其它窗口
    win.mainloop()  # 并开启一个嵌套事件循环进行等待
    print('dialog exit!')

root = Tk()
Button(root, text='popup', command=dialog).pack()
root.mainloop()
