"""
Build GUI with tkinter with buttons that change color and grow
"""
import random
from tkinter import *

FontSize = 25
Colors = ['red', 'green', 'blue', 'yellow', 'orange', 'white', 'cyan', 'purple']


def reply(text):
    print(text)
    popup = Toplevel()
    color = random.choice(Colors)
    Label(popup, text='Popup', bg='black', fg=color).pack()
    L.config(fg=color)


def timer():
    L.config(fg=random.choice(Colors))
    win.after(250, timer)


def grow():
    global FontSize
    FontSize += 5
    L.config(font=('arial', FontSize, 'italic'))
    win.after(100, grow)


if __name__ == '__main__':
    win = Tk()
    L = Label(win, text='Spam', font=('arial', FontSize, 'italic'), fg='yellow', bg='navy', relief=RAISED)
    L.pack(side=TOP, expand=YES, fill=BOTH)
    Button(win, text='press', command=(lambda: reply('red'))).pack(side=BOTTOM, fill=X)
    Button(win, text='timer', command=timer).pack(side=BOTTOM, fill=X)
    Button(win, text='grow', command=grow).pack(side=BOTTOM, fill=X)
    win.mainloop()
