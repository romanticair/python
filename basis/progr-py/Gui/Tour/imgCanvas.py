from tkinter import *

gifdir = "..\Images\\"

win = Tk()
img = PhotoImage(file=gifdir + "animal.png")
can = Canvas(win)
can.pack(fill=BOTH)
can.create_image(2, 2, image=img, anchor=NW)  # x和y坐标
win.mainloop()
