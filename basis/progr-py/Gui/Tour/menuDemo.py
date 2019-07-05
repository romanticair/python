#!/usr/local/bin/python

"""
menu/tool bars packed before middle, fii=X (pack first=clip last);
adds photo menu entries; see also: add_checkbutton, add_radiobutton.
"""

from tkinter import *
from tkinter.messagebox import *


class NewMenuDemo(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.createWidgets()
        self.master.title('Toolbars and Menus')    # set window-manager info
        self.master.iconname('tkpython')           # label when iconified

    def createWidgets(self):
        self.makeMenuBar()
        self.makeToolBar()
        l = Label(self, text='Menu and Toolbar Demo')
        l.config(relief=SUNKEN, width=40, height=10, bg='white')
        l.pack(expand=YES, fill=BOTH)

    def makeToolBar(self):
        toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
        toolbar.pack(side=BOTTOM, fill=X)
        Button(toolbar, text='Quit', command=self.quit).pack(side=RIGHT)
        Button(toolbar, text='Hello', command=self.greeting).pack(side=LEFT)

    def makeMenuBar(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu()
        self.editMenu()
        self.imageMenu()

    def fileMenu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Open...', command=self.notdone)
        pulldown.add_command(label='Quit', command=self.quit)
        self.menubar.add_cascade(label='File', underline=0, menu=pulldown)

    def editMenu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Paste', command=self.notdone)
        pulldown.add_command(label='Spam', command=self.greeting)
        pulldown.add_separator()
        pulldown.add_command(label='Delete', command=self.greeting)
        pulldown.entryconfig(4, state=DISABLED)
        self.menubar.add_cascade(label='Edit', underline=0, menu=pulldown)

    def imageMenu(self):
        photoFiles = ('small1.png', 'tree.png', 'people.png')
        pulldown = Menu(self.menubar)
        self.photoObjs = []
        for file in photoFiles:
            img = PhotoImage(file='../Images/' + file)
            pulldown.add_command(image=img, command=self.notdone)
            self.photoObjs.append(img)
        self.menubar.add_cascade(label='Image', underline=0, menu=pulldown)

    def greeting(self):
        showinfo('greeting', 'Greeting')

    def notdone(self):
        showerror('Not implemented', 'Not yet avaiable')

    def quit(self):
        if askyesno('Verify quit', 'Are you sure you want to quit?'):
            Frame.quit(self)

if __name__ == '__main__':
    NewMenuDemo().mainloop()
