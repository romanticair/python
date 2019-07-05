"""
使用标准tkinter图片对象显示一张图片；
这个可以处理GIF图像文件，但是不支持JPEG图像文件；
图像文件名称在命令行列出来，或者采用默认设置；
使用Canvas而不是Label来滚动等。
"""
import os, sys
from tkinter import *

imgdir = "..\Images\\"
imgfile = 'animal.png'

if len(sys.argv) > 1:
    imgfile = sys.argv[1]

imgpath = os.path.join(imgdir, imgfile)

win = Tk()
win.title(imgfile)
imgobj = PhotoImage(file=imgpath)
Label(win, image=imgobj).pack()
print(imgobj.width(), imgobj.height())
win.mainloop()
