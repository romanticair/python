"""
#################################################################################
幻灯片放映：Python/tkinter 中一个简单的照片图像幻灯片放映；
设置基础特征的代码如下，它们可以在子类中扩展。
#################################################################################
"""

import random
from tkinter import *
from glob import glob
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename

SIZE = (450, 450)                          # 启动和幻灯片放映开始时画布的高度、宽度
imageTypes = [('Gif files', '.gif'),       # 用于文件打开对话框
              ('Ppm files', '.ppm'),       # jpg加上一个Tk补丁
              ('Pgm files', '.pgm'),       # 位图加上位图图像
              ('Png files', '.png'),
              ('All files', '*')]


class SlideShow(Frame):
    def __init__(self, parent=None, picdir='.', msecs=3000, size=SIZE, **args):
        Frame.__init__(self, parent, **args)
        self.size = size
        self.msecs = msecs
        self.beep = True
        self.drawn = None
        self.makeWidgets()
        self.pack(expand=YES, fill=BOTH)
        self.opens = picdir
        files = []
        for label, ext in imageTypes[:-1]:
            files = files + glob('%s/*%s' % (picdir, ext))
        self.images = [(x, PhotoImage(file=x)) for x in files]

    def makeWidgets(self):
        height, width = self.size
        self.canvas = Canvas(self, bg='white', height=height, width=width)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.onoff = Button(self, text='Start', command=self.onStart)
        self.onoff.pack(fill=X)
        Button(self, text='Open', command=self.onOpen).pack(fill=X)
        Button(self, text='Beep', command=self.onBeep).pack(fill=X)
        Button(self, text='Quit', command=self.onQuit).pack(fill=X)

    def onStart(self):
        self.loop = True
        self.onoff.config(text='Stop', command=self.onStop)
        self.canvas.config(height=self.size[0], width=self.size[1])
        self.onTimer()

    def onStop(self):
        self.loop = False
        self.onoff.config(text='Start', command=self.onStart)

    def onOpen(self):
        self.onStop()
        name = askopenfilename(initialdir=self.opens, filetypes=imageTypes)
        if name:
            if self.drawn:
                self.canvas.delete(self.drawn)
            img = PhotoImage(file=name)
            self.canvas.config(height=img.height(), width=img.width())
            self.drawn = self.canvas.create_image(2, 2, image=img, anchor=NW)
            self.image = name, img

    def onQuit(self):
        self.onStop()
        self.update()
        if askyesno('PyView', 'Really quit now?'):
            self.quit()

    def onBeep(self):
        self.beep = not self.beep  # toggle, or use ^ 1

    def onTimer(self):
        if self.loop:
            self.drawNext()
            self.after(self.msecs, self.onTimer)

    def drawNext(self):
        if self.drawn:
            self.canvas.delete(self.drawn)
        name, img = random.choice(self.images)
        self.drawn = self.canvas.create_image(2, 2, image=img, anchor=NW)
        self.image = name, img
        if self.beep:
            self.bell()
        self.canvas.update()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        picdir = sys.argv[1]
    else:
        picdir = r'L:\MyPythonProgr\BooksLearningRecords\ProgrammingPython\Gui\Images'
    root = Tk()
    root.title('PyView 1.2')
    root.iconname('PyView')
    Label(root, text='Python Slide Show Viewer').pack()
    SlideShow(root, picdir=picdir, bd=3, relief=SUNKEN)
    root.mainloop()
