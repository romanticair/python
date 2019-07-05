from tkinter import *

root = Tk()
labelfont = ('time', 20, 'bold')                     # 字体系列、大小、类型
widget = Label(root, text='Hello config world')
widget.config(bg='black', fg='yellow')               # 在黑色标签上显示黄色文体
widget.config(font=labelfont)                        # 使用更大的字体
widget.config(height=3, width=20)                   # 初始化大小：行间距、字符间距
widget.pack(expand=YES, fill=BOTH)
root.mainloop()
