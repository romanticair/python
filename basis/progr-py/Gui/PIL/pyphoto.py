"""
#####################################################################################
PyPhoto 1.1: 缩略图图像浏览器支持吊证大小并保存

支持多种图像目录缩略窗口 ----- 最初的图像目录当成 cmd 参数传入，使用默认的 "图像"，
或通过主窗口按键被选取；在图像视图或缩略图窗口中按下 "D" 打开之后的目录。

浏览器也滚动弹出的图像，对屏幕来说这些图像太大了，仍然要做：
(1) 窗口调整大小时，根据当前窗口的大小重新排列缩略图；
(2) [已做]调整图像大小以适应当前窗口大小的选项?
(3) 如果图像尺寸小于窗口的最大尺寸则要避免滚动(若图像宽 <= 屏幕宽而且图像高 <= 屏幕高,
    则使用标签?)

若单击一下图像，调整图像尺寸至其中一个显示器的尺寸，在按键时以 10% 的增量进行放大或缩
小；普及开。
警告：多次调整大小后，(图像)质量、像素似乎会受损(这可能是PIL的缺陷)

以下的定标器改编自PIL的缩略图代码，它和此处的定标器屏幕高度相似，但只能缩小；
x, y = igmwide, imghigh
if x > scrwide:
    y = max(y * scrwide // x, 1)
    x = scrwide
if y > scrhigh:
    x = max(x * scrhigh // y, 1)
    x = scrhigh
#####################################################################################
"""

import sys
import math
import os
from tkinter import *
from tkinter.filedialog import SaveAs, Directory
from PIL import Image                                 # PIL图像：也在tkinter中
from PIL.ImageTk import PhotoImage                    # PIL图像部件更换，支持更多格式
from Gui.Tour.viewer_thumbs import makeThumbs         # 制作缩略图

# 记住跨所有窗口的最后目录
saveDialog = SaveAs(title='Save As (filename gives image type)')
openDialog = Directory(title='Select Image Directory To Open')

trace = print                                          # 或者 lambda *arg: None
appname = 'PyPhoto 1.1: '


class ScrolledCanvas(Canvas):
    """
    一个容器中的画布是已为自己制造自动垂直和水平滚动栏
    """
    def __init__(self, container):
        Canvas.__init__(self, container)
        self.config(borderwidth=0)

        vbar = Scrollbar(container)
        hbar = Scrollbar(container, orient='horizontal')
        vbar.pack(side=RIGHT, fill=Y)              # 在栏后面打包画布
        hbar.pack(side=BOTTOM, fill=X)             # 因此先裁剪
        self.pack(side=TOP, fill=BOTH, expand=YES)

        vbar.config(command=self.yview)            # 调用滚动步骤
        hbar.config(command=self.xview)
        self.config(yscrollcommand=vbar.set)       # 调用画布步骤
        self.config(xscrollcommand=hbar.set)


class ViewOne(Toplevel):
    """
    创建时，在弹出窗口打开一个单独的图像；由于照片图像对象必须保存类，否则回收
    就要背擦除；如果太大而不能显示则进行滚动，鼠标点击调整窗口的高度或宽度：伸展
    或收缩：I/O 按键进行 放大/缩小，这两者的调整大小方案维持了原始宽度高比，代码
    在此被分解，以尽可能的避免冗余。
    """
    def __init__(self, imgdir, imgfile, forcesize=()):
        Toplevel.__init__(self)
        helptext = '(click L/R or press I/O to resize, S to save, D to open)'
        self.title(appname + imgfile + ' ' + helptext)
        imgpath = os.path.join(imgdir, imgfile)
        imgpil = Image.open(imgpath)
        self.canvas = ScrolledCanvas(self)
        self.drawImage(imgpil, forcesize)
        self.canvas.bind('<Button-1>', self.onSizeToDisplayHeight)
        self.canvas.bind('<Button-3>', self.onSizeToDisplayWidth)
        self.bind('<KeyPress-i>', self.onZoomIn)
        self.bind('<KeyPress-o>', self.onZoomOut)
        self.bind('<KeyPress-s>', self.onSaveImage)
        self.bind('<KeyPress-d>', onDirectoryOpen)
        self.focus()

    def drawImage(self, imgpil, forcesize=()):
        imgtk = PhotoImage(image=imgpil)                      # 非文件 = 图像路径
        scrwide, scrhigh = forcesize or self.maxsize()        # wm 屏幕大小 x,y
        imgwide = imgtk.width()                               # 像素大小
        imghigh = imgtk.height()                              # 和 imgpil.size 一样

        fullsize = (0, 0, imgwide, imghigh)                   # 可滚动的
        viewwide = min(imgwide, scrwide)                      # 可浏览的
        viewhigh = min(imghigh, scrhigh)

        canvas = self.canvas
        canvas.delete('all')                                  # 清除先前的照片
        canvas.config(height=viewhigh, width=viewwide)        # 可浏览的窗口大小
        canvas.config(scrollregion=fullsize)                  # 可滚动的区域大小
        canvas.create_image(0, 0, image=imgtk, anchor=NW)

        if imgwide <= scrwide and imghigh <= scrhigh:        # 太大不能显示?
            self.state('normal')                              # 否: 赢得每个图像的大小
        if sys.platform[:3] == 'win':                         # 窗口全屏
            self.state('zoomed')                              # 其它使用 geometry()
        self.saveimage = imgpil
        self.savephoto = imgtk                                # 一直参考我
        trace((scrwide, scrhigh), imgpil.size)

    def sizeToDisplaySide(self, scaler):
        # resize to fill one size of the display
        imgpil = self.saveimage
        scrwide, scrhigh = self.maxsize()                     # wm 屏幕大小 x,y
        imgwide, imghigh = imgpil.size                        # 像素中图像的大小
        newwide, newhigh = scaler(scrwide, scrhigh, imgwide, imghigh)
        if newwide * newhigh < imgwide * imghigh:
            filter = Image.ANTIALIAS                          # shrink: 缩小: 抗锯齿
        else:                                                # grow: 扩展: bicub 更清晰
            filter = Image.BICUBIC
        imgnew = imgpil.resize((newwide, newhigh), filter)
        self.drawImage(imgnew)

    def onSizeToDisplayHeight(self, event):
        def scaleHigh(scrwide, scrhigh, imgwide, imghigh):
            newhigh = scrhigh
            newwide = int(scrhigh * (imgwide / imghigh))      # 3.x 真的 div
            return newwide, newhigh                          # 成比例的
        self.sizeToDisplaySide(scaleHigh)

    def onSizeToDisplayWidth(self, event):
        def scaleWide(scrwide, scrhigh, imgwide, imghigh):
            newhigh = scrwide
            newwide = int(scrwide * (imghigh / imgwide))      # 3.x 真的 div
            return newwide, newhigh                          # 成比例的
        self.sizeToDisplaySide(scaleWide)

    def zoom(self, factor):
        # zoom in or out in increments
        imgpil = self.saveimage
        wide, high = imgpil.size
        if factor < 1.0:                                     # 如果缩小, 抗锯齿最佳
            filter = Image.ANTIALIAS                         # 也是最近的，双线性的
        else:
            filter = Image.BICUBIC
        new = imgpil.resize((int(wide * factor), int(high * factor)), filter)
        self.drawImage(new)

    def onZoomIn(self, event, incr=0.10):
        self.zoom(1.0 + incr)

    def onZoomOut(self, event, decr=0.10):
        self.zoom(1.0 - decr)

    def onSaveImage(self, event):
        # 将当前的图像状态保存至文件
        filename = saveDialog.show()
        if filename:
            self.saveimage.save(filename)


def onDirectoryOpen(event):
    """
    在可用缩略图和图像新窗口中打开一个新的图像目录
    """
    dirname = openDialog.show()
    if dirname:
        viewThumbs(dirname, kind=Toplevel)


def viewThumbs(imgdir, kind=Toplevel, numcols=None, height=400, width=500):
    """
    制造主要的或弹出的缩略图按键窗口，使用固定大小的按键，可滚动的画布；
    设置可滚动的(全)尺寸和位置，画布中缩略图的横轴坐标，不在假设所有的缩
    略图都是同样的大小，得到所有缩略图的最大值(横，纵)，有些可能小点儿。
    """
    win = kind()
    helptxt = '(press D to open other)'
    win.title(appname + imgdir + ' ' + helptxt)
    quit = Button(win, text='Quit', command=win.quit, bg='beige')
    quit.pack(side=BOTTOM, fill=X)
    canvas = ScrolledCanvas(win)
    canvas.config(height=height, width=width)                      # 可浏览窗口大小的初始化
                                                                   # 如果用户调整大小则有变动
    thumbs = makeThumbs(imgdir)                                    # [(图像文件，图像对象)]
    numthumbs = len(thumbs)
    if not numcols:
        numcols = int(math.ceil(math.sqrt(numthumbs)))             # 固定的或 N x N
    numrows = int(math.ceil(numthumbs / numcols))                  # 3.x 真的 div

    # 最大的宽和高之比: thumb = (name, obj), thumb.size = (width, height)
    linksize = max(max(thumb[1].size) for thumb in thumbs)
    trace(linksize)
    fullsize = (0, 0, (linksize * numcols), (linksize * numrows))  # 左上角x,y 右下角x,y
    canvas.config(scrollregion=fullsize)                           # 可滚动的区域范围

    rowpos = 0
    savephotots = []
    while thumbs:
        thumbsrow, thumbs = thumbs[:numcols], thumbs[numcols:]
        colpos = 0
        for (imgfile, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj)
            link = Button(canvas, image=photo)

            def handler(savefile=imgfile):
                ViewOne(imgdir, savefile)
            link.config(command=handler, width=linksize, height=linksize)
            link.pack(side=LEFT, expand=YES)
            canvas.create_window(colpos, rowpos, anchor=NW, window=link, width=linksize, height=linksize)
            colpos += linksize
            savephotots.append(photo)
        rowpos += linksize

    win.bind('<KeyPress-d>', onDirectoryOpen)
    win.savephotos = savephotots
    return win

if __name__ == '__main__':
    """
    打开目录 = 默认的或命令行参数
     否则显示简单的窗口以选择
    """
    # imgdir = r'../Images/'
    imgdir = ''
    if len(sys.argv) > 1:
        imgdir = sys.argv[1]
    if os.path.exists(imgdir):
        mainwin = viewThumbs(imgdir, kind=Tk)
    else:
        mainwin = Tk()
        mainwin.title(appname + 'Open')
        handler = lambda: onDirectoryOpen(None)
        Button(mainwin, text='Open Image Directory', command=handler).pack()
    mainwin.mainloop()
