"""
程序的单选和复选按钮栏类，能够在之后获取状态；
传递选项列表，调用state()方法，自动化变量细节
"""
from tkinter import *


class CheckBar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return [var.get() for var in self.vars]


class RadioBar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.var = StringVar()
        self.var.set(picks[0])
        for pick in picks:
            rad = Radiobutton(self, text=pick, value=pick, variable=self.var)
            rad.pack(side=side, anchor=anchor, expand=YES)

    def state(self):
        return self.var.get()

if __name__ == '__main__':
    root = Tk()
    lng = CheckBar(root, ['Python', 'C#', 'Jave', 'C++'])
    gui = RadioBar(root, ['win', 'x11', 'mac'], side=TOP, anchor=NW)
    tgl = CheckBar(root, ['All'])

    gui.pack(side=LEFT, fill=Y)
    lng.pack(side=TOP, fill=X)
    tgl.pack(side=LEFT)
    lng.config(relief=GROOVE, bd=2)
    gui.config(relief=RIDGE, bd=2)

    def allstates():
        print(gui.state(), lng.state(), tgl.state())

    from quitter import Quitter
    Quitter(root).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
    root.mainloop()



