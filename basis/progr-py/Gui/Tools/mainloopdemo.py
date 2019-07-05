"""
两个不同的主循环调用示例；各个调用在主窗口关闭后返回；由于不再使用图形用户界面，
用户结果存储在Python对象中；图形用户界面通常对小组进行配置，然后仅允许一个主循环，
界面的逻辑存在于调用；本示例程序使用主循环调用来实现来自于非图形用户界面的主程序
的两次用户模式交互，展示了一种向已有的非图形用户界面脚本中添加图形用户界面组件的
方法。
"""

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Demo(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        Label(self, text='Basic demos').pack()
        Button(self, text='open', command=self.openfile).pack(fill=BOTH)
        Button(self, text='save', command=self.savefile).pack(fill=BOTH)
        self.open_name = self.save_name = ''

    def openfile(self):                    # 存储用户结果
        self.open_name = askopenfilename()   # 这里使用对话框选项

    def savefile(self):
        self.save_name = asksaveasfilename()

if __name__ == '__main__':
    # 显示窗口一个
    print('popup1...')
    mydialog = Demo()
    mydialog.mainloop()                      # 显示，窗口关闭后返回
    print(mydialog.open_name)                # 尽管图形用户界面已消失，名称依然存在于对象中
    print(mydialog.save_name)
    # 程序的非图形用户界面部分使用这里的mydialog

    # 再次显示窗口
    print('popup2...')
    mydialog = Demo()
    mydialog.mainloop()
    print(mydialog.open_name)
    print(mydialog.save_name)
