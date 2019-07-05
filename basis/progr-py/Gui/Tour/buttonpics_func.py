from tkinter import *
from glob import glob                     # 文件名扩展列表
import demoCheck                           # 向me附加一个复选按钮示例
import random                              # 随机挑选一个图片

gifdir = "..\Images\\"


def draw():
    name, photo = random.choice(images)
    lbl.config(text=name)
    pix.config(image=photo)

root = Tk()
lbl = Label(root, text='none', bg='blue', fg='red')
pix = Button(root, text='Press me', command=draw, bg='white')
lbl.pack(fill=BOTH)
pix.pack(pady=10)
demoCheck.Demo(root, relief=SUNKEN, bd=2).pack(fill=BOTH)

files = glob(gifdir + '*.png')                                  # 当前的PNG
images = [(x, PhotoImage(file=x)) for x in files]              # 载入并保存
print(files)
root.mainloop()
