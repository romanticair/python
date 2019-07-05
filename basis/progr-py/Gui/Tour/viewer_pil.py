"""
使用PIL图像替代对象显示一个图片
可处理更多类型的图片；
"""

import os
import sys
from tkinter import *
from PIL.ImageTk import PhotoImage                  # 使用PIL替代类

imgdir = "..\Images\\"
imgfile = 'sport.jpg'                                 # 多种格式都可以用
if len(sys.argv) > 1:
    imgfile = sys.argv[1]

imgpath = os.path.join(imgdir, imgfile)

win = Tk()
win.title(imgfile)
imgobj = PhotoImage(file=imgpath)
Label(win, image=imgobj).pack()
win.mainloop()
print(imgobj.width(), imgobj.height())
