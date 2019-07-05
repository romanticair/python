# 同前，但在after()计时器回调之后隐藏或显示整个窗口

from tkinter import *
import alarm


class Alarm(alarm.Alarm):
    def repeater(self):
        self.bell()
        if self.master.state() == 'normal':  # 窗口有没有显示
            self.master.withdraw()           # 隐藏整个窗口，没有图标
        else:                               # iconfiy shrinks to an icon
            self.master.deiconify()          # 否则刷新整个窗口
            self.master.lift()               # 并出现在顶层
        self.after(self.msecs, self.repeater)

if __name__ == '__main__':
    Alarm(msecs=1000).mainloop()
