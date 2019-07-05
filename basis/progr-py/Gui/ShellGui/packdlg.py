# 弹出图形化对话框，供选择打包脚本参数的输入，并运行

from glob import glob
from tkinter import *
from packer import pack                                         # 使用pack脚本中的模块
from formrows import makeFormRow                                # 使用表单构建工具


def packDialog():
    win = Toplevel()                                              # 行的顶层窗口
    win.title('Enter Pack Parameters')                            # 有2行图文框，还带有"OK"按钮
    var1 = makeFormRow(win, label='Output file')
    var2 = makeFormRow(win, label='Files to pack', extend=True)
    Button(win, text='OK', command=win.destroy).pack()
    win.grab_set()
    win.focus_set()                                               # 动作：鼠标选取数据；键盘获得焦点；等待
    win.wait_window()                                             # 等到窗口销毁，否则立即返回
    return var1.get(), var2.get()                                # 获取相关联的变量值


def runPackDialog():
    output, patterns = packDialog()
    if output != '' and patterns != '':
        patterns = patterns.split()
        filenames = []
        for sublist in map(glob, patterns):
            filenames += sublist
        print('Packer:', output, filenames)
        pack(ofile=output, ifiles=filenames)

if __name__ == '__main__':
    root = Tk()
    Button(root, text='popup', command=runPackDialog).pack(fill=X)
    Button(root, text='quit', command=root.quit).pack(fill=X)
    root.mainloop()
