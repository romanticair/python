"a simple customizable scrolled listbox component"
from tkinter import *


class ScrolledList(Frame):
    def __init__(self, options, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makeWidgets(options)

    def handerList(self, event):
        index = self.listbox.curselection()       # on list double-click
        label = self.listbox.get(index)           # fetch selection text
        self.runCommand(label)                    # and call action here

    def makeWidgets(self, options):
        sbar = Scrollbar(self)
        list = Listbox(self, relief=SUNKEN)
        sbar.config(command=list.yview)           # xlink sbar and list
        list.config(yscrollcommand=sbar.set)      # move one move other
        sbar.pack(side=RIGHT, fill=Y)             # pack first=clip last
        list.pack(side=LEFT, expand=YES, fill=BOTH)  # list clipped first
        pos = 0
        for label in options:                    # add to listbox
            list.insert(pos, label)               # or insert(END, label)
            pos += 1
        # list.config(selectmode=SINGLE, setgrid=1) # select, resize modes
        list.bind('<Double-1>', self.handerList)  # set event handler
        self.listbox = list

    def runCommand(self, selection):            # redefine me lower
        print('You selected:', selection)

if __name__ == '__main__':
    options = (('Lumberjack-%s' % x) for x in range(20))
    ScrolledList(options).mainloop()
