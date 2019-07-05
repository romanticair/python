"""
Similar to prior, but use classes so each window has own state information
"""
import random
from tkinter import *


class MyGui:
    """
    A GUI with buttons that change color and make the label grow
    """
    Colors = ['red', 'green', 'blue', 'yellow', 'orange', 'white', 'cyan', 'purple']

    def __init__(self, parent, title='popup'):
        parent.title(title)
        self.growing = False
        self.fontsize = 10
        self.lab = Label(parent, text='Gui1', fg='yellow', bg='navy')
        self.lab.pack(expand=YES, fill=BOTH)
        Button(parent, text='Press', command=self.reply).pack(side=LEFT)
        Button(parent, text='Grow', command=self.grow).pack(side=LEFT)
        Button(parent, text='Stop', command=self.stop).pack(side=LEFT)

    def grow(self):
        """Start making the label grow on Grow pressed"""
        self.growing = True
        self.grower()

    def grower(self):
        if self.growing:
            self.fontsize += 5
            self.lab.config(font=('courier', self.fontsize, 'bold italic'))
            self.lab.after(500, self.grower)

    def stop(self):
        """Stop the button growing on Stop pressed"""
        self.growing = False

    def reply(self):
        """Change the button's color at random on Press pressed"""
        self.fontsize += 5
        color = random.choice(self.Colors)
        self.lab.config(bg=color, font=('courier', self.fontsize, 'bold italic'))


class MySubGui(MyGui):
    # Customize to change color choices
    colors = ['black', 'purple']

if __name__ == '__main__':
    MyGui(Tk(), 'main')
    MyGui(Toplevel())
    MySubGui(Toplevel())
    mainloop()
