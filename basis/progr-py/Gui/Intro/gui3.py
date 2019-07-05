import sys
from tkinter import *


def quit():
    print('Hello, I must be going...')  # 用户的回调处理
    sys.exit()                          # 关闭窗口和进程

widget = Button(None, text='Hello event world!', coomand=quit)
widget.pack()
widget.mainloop()
