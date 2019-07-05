# resize toolbar images on the fly with PIL

from tkinter import *
from PIL.ImageTk import PhotoImage, Image


def makeToolBar(self, size=(40, 40)):
    imgdir = r'../Images/'
    toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
    toolbar.pack(side=BOTTOM, fill=X)
    photos = 'small2.png', 'small3.png', 'people.png'
    self.toolPhotoObjs = []
    for file in photos:
        imgobj = Image.open(imgdir + file)          # make new thumb
        imgobj.thumbnail(size, Image.ANTIALIAS)     # best downsize filter
        img = PhotoImage(imgobj)
        btn = Button(toolbar, image=img, command=self.greeting)
        btn.config(relief=RAISED, bd=2)
        btn.config(width=size[0], height=size[1])
        btn.pack(side=LEFT)
        self.toolPhotoObjs.append((img, imgobj))
    Button(toolbar, text='Quit', command=self.quit).pack(side=RIGHT, fill=Y)

if __name__ == '__main__':
    from menuDemo import NewMenuDemo
    NewMenuDemo.makeToolBar = makeToolBar
    NewMenuDemo().mainloop()
