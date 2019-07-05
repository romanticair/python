from tkinter import *

gifdir = "..\Images\\"

win = Tk()
img = PhotoImage(file=gifdir + "animal.png")
Button(win, image=img).pack()
win.mainloop()
