from sys import argv
from tkinter import *

gifdir = "..\Images\\"
filename = argv[1] if len(argv) > 1 else "animal.png"

win = Tk()
img = PhotoImage(file=gifdir + filename)
can = Canvas(win)
can.pack(fill=BOTH)
can.config(width=img.width(), height=img.height())       # size to img size
can.create_image(2, 2, image=img, anchor=NW)
win.mainloop()
