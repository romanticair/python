from tkinter import *

root = Tk()
widget = Label(root)
# 更通用的办法是，组件创建后，调用组件的config方法进行选项设置，如下
widget.config(text='Hello GUI world!')
# 可以在任何时间被调用
widget.pack(side=TOP, expand=YES, fill=BOTH)
root.title('gui1g.py')
root.mainloop()
