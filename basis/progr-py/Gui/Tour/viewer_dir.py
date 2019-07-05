"""
在弹出窗口中显示同一目录下的所有图像
基础tkinter支持gif，但是没安装PIP的话会跳过JPEG
"""
import os
import sys
from tkinter import *
from PIL.ImageTk import PhotoImage

imgdir = "..\Images\\"
if len(sys.argv) > 1:
    imgdir = sys.argv[1]

imgfiles = os.listdir(imgdir)  # 不包括目录前缀

main = Tk()
main.title('Viewer')
quit = Button(main, text='Quit all', command=main.quit, font=('courier', 25))
quit.pack()
savephotos = []

for imgfile in imgfiles:
    imgpath = os.path.join(imgdir, imgfile)
    win = Toplevel()
    win.title(imgfile)
    try:
        imgobj = PhotoImage(file=imgpath)
        Label(win, image=imgobj).pack()
        print(imgpath, imgobj.width(), imgobj.height())
        savephotos.append(imgobj)
    except:
        errmsg = 'skipping %s \n%s' % (imgfile, sys.exc_info()[1])
        Label(win, text=errmsg).pack()

mainloop()
