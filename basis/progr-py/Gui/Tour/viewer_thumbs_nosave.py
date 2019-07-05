"""
其它步骤一样，但是在内存中创建缩略图文件时，既不存储图片文件，也不从文件载入；
对于小目录来说看起来存储和载入速度很快，但是保存至文件的方法使大图片集的启动速度变快；
在某些应用程序（网页）中，可能需要存储图片；
"""
import os, sys
from PIL import Image
from tkinter import Tk
import viewer_thumbs


def makeThumbs(imgdir, size=(100, 100), subdir='thumbs'):
    """在内存中创建缩略图，而不需要缓存到文件中"""
    thumbs = []
    for imgfile in os.listdir(imgdir):
        imgpath = os.path.join(imgdir, imgfile)
        try:
            imgobj = Image.open(imgpath)  # 创建新的缩略图
            imgobj.thumbnail(size)
            thumbs.append((imgfile, imgobj))
        except:
            print('Skipping:', imgpath)
        return thumbs

if __name__ == '__main__':
    imgdir = (len(sys.argv) > 1 and sys.argv[1]) or '..\Images\\'
    viewer_thumbs.makeThumbs = makeThumbs
    main, save = viewer_thumbs.viewer(imgdir, kind=Tk)
    main.mainloop()
