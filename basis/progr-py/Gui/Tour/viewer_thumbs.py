"""
显示一个目录下的所有的图像为缩略图图片按钮，在按钮被按下时，展示原始大小的图片；
需要PIL用于JPEG的显示和缩略图的创建；
需要做的是：如果窗口需要展示太多缩略图，则添加滚动效果！
"""

import os, sys, math
from tkinter import *
from PIL import Image
from PIL.ImageTk import PhotoImage


def makeThumbs(imgdir, size=(100, 100), subdir='thumbs'):
    """
    获取一个目录下的所有图像的缩略图，对于每一个图像，创建并保存一个新的缩略图，
    或者载入并且返回一个已有的缩略图；如有需要，创建缩略图目录；返回一个格式为
    (图像文件名称，缩略图图像对象)的列表；调用器也能够在缩略图目录上运行listdir
    以执行载入；不支持的文件类型可能会引起IOError，或者其他错误；
    警告：也会检查文件的时间戳；
    """
    thumbdir = os.path.join(imgdir, subdir)
    if not os.path.exists(thumbdir):
        os.mkdir(thumbdir)

    thumbs = []
    for imgfile in os.listdir(imgdir):
        thumbpath = os.path.join(thumbdir, imgfile)
        if os.path.exists(thumbpath):
            thumobj = Image.open(thumbpath)
            thumbs.append((imgfile, thumobj))
        else:
            print('making', thumbpath)
            imgpath = os.path.join(imgdir, imgfile)
            try:
                imgobj = Image.open(imgpath)               # 创建新的缩略图
                imgobj.thumbnail(size, Image.ANTIALIAS)    # 最好的缩小尺寸过滤器
                imgobj.save(thumbpath)                     # 通过ext或者传入的类型
                thumbs.append((imgfile, imgobj))
            except:
                print('Skipping:', imgpath)
    return thumbs


class ViewOne(Toplevel):
    """
    在创建时，在一个弹出窗口中打开一个图片；
    Photo Image对象必须保存：如果对象被重新声明，图像会被清除；
    """
    def __init__(self, imgdir, imgfile):
        Toplevel.__init__(self)
        self.title(imgfile)
        imgpath = os.path.join(imgdir, imgfile)
        imgobj = PhotoImage(file=imgpath)
        Label(self, image=imgobj).pack()
        print(imgpath, imgobj.width(), imgobj.height())     # 像素大小
        self.savephoto = imgobj                             # 保留对图片的引用


def viewer(imgdir, kind=Toplevel, cols=None):
    """
    为一个图像目录创建缩略图链接窗口：每一个图像创建一个缩略图按钮；
    使用kind=Tk以便在主应用程序窗口或Frame容器(封装)中显示；
    每一个循环的imgfile都有所不同：必须默认保存；PhotoImage对象必须被保存；
    如果对象被重新声明，则会清楚；封装的行框架(与网格、固定大小和画布相对)
    """
    win = kind()
    win.title('Viewer:' + imgdir)
    quit = Button(win, text='Quit', command=win.quit, bg='beige')  # 首先封装
    quit.pack(fill=X, side=BOTTOM)                                 # 像这样，最后clip
    thumbs = makeThumbs(imgdir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))              # 固定大小，或者N x N

    savephotos = []
    while thumbs:
        thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
        row = Frame(win)
        row.pack(fill=BOTH)
        for (imgfile, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj)
            link = Button(row, image=photo)
            handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
            link.config(command=handler)
            link.pack(side=LEFT, expand=YES)
            savephotos.append(photo)
    return win, savephotos

if __name__ == '__main__':
    imgdir = (len(sys.argv) > 1 and sys.argv[1]) or '..\Images\\'
    main, save = viewer(imgdir, kind=Tk)
    main.mainloop()



