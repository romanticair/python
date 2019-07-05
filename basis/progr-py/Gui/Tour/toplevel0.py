import sys
from tkinter import Toplevel, Button, Label

win1 = Toplevel()                # 两个独立的窗口
win2 = Toplevel()                # 但是在同一进程
Button(win1, text='Spam', command=sys.exit).pack()
Button(win2, text='SPAM', command=sys.exit).pack()
Label(text='Popups').pack()      # 默认的Tk()根窗口
win1.mainloop()
