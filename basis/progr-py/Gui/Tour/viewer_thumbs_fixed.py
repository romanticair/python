"""
使用固定大小的缩略图，这样才能对齐；来自图片对象的大小，假设所有缩略图都
具有相同的尺寸；这就是文件选择器的GUI的功能；
"""
import sys, math
from tkinter import *
from PIL.ImageTk import PhotoImage
from viewer_thumbs import makeThumbs, ViewOne


def viewer(imgdir, kind=Toplevel, cols=None):
    """
    自定义版本，能够使用固定大小的按钮进行布局
    """
    win = kind()
    win.title('Viewer:' + imgdir)
    thumbs = makeThumbs(imgdir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))   # 固定大小，或者N x N

    savephotos = []
    while thumbs:
        thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
        row = Frame(win)
        row.pack(fill=BOTH)
        for (imgfile, imgobj) in thumbsrow:
            size = max(imgobj.size)                     # 宽度，高度
            print(size)
            photo = PhotoImage(imgobj)
            link = Button(row, image=photo)
            handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
            link.config(command=handler, width=size, height=size)
            link.pack(side=LEFT, expand=YES)
            savephotos.append(photo)

    Button(win, text='Quit', command=win.quit, bg='beige').pack(fill=X)
    return win, savephotos

if __name__ == '__main__':
    imgdir = (len(sys.argv) > 1 and sys.argv[1]) or '..\Images\\'
    main, save = viewer(imgdir, kind=Tk)
    main.mainloop()