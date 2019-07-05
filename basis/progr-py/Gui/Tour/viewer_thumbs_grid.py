
"""
与viewer_thumbs相同，但是使用grid几何管理器以尝试达到更整齐的布局效果；
通常通过框架和封装能够达到相同的效果，如果按你大小全都固定或者一致的话；
"""
import sys, math
from tkinter import *
from PIL.ImageTk import PhotoImage
from viewer_thumbs import makeThumbs, ViewOne


def viewer(imgdir, kind=Toplevel, cols=None):
    """
    使用网格的自定义版本
    """
    win = kind()
    win.title('Viewer:' + imgdir)
    thumbs = makeThumbs(imgdir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))   # 固定大小，或者N x N

    rownum = 0
    savephotos = []
    while thumbs:
        thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
        column = 0
        for (imgfile, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj)
            link = Button(win, image=photo)
            handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
            link.config(command=handler)
            link.grid(row=rownum, column=column)
            savephotos.append(photo)
            column += 1
        rownum += 1

    Button(win, text='Quit', command=win.quit).grid(columnspan=cols, stick=EW)
    return win, savephotos

if __name__ == '__main__':
    imgdir = (len(sys.argv) > 1 and sys.argv[1]) or '..\Images\\'
    main, save = viewer(imgdir, kind=Tk)
    main.mainloop()
