# 检测线程回调队列，但针对操作和回调使用类的绑定方法

import time
from tkinter.scrolledtext import ScrolledText
from threadtools import threadChecker, startThread


class MyGui:
    def __init__(self, reps=3):
        self.reps = reps
        self.text = ScrolledText()
        self.text.pack()
        threadChecker(self.text)
        self.text.bind('<Button-1>', lambda event: list(map(self.onEvent, range(6))))

    def onEvent(self, i):
        myname = 'thread-%s' % i
        startThread(action=self.threadaction,
                    args=(i, 3),
                    context=(myname,),
                    onExit=self.threadexit,
                    onFail=self.threadfail,
                    onProgress=self.threadprogress)

    # 线程主要操作
    def threadaction(self, id, progress):     # 线程的功能
        for i in range(self.reps):
            time.sleep(1)
            if progress:
                progress(i)                      # 回调，加入队列
        if id % 2 == 1:                          # 奇数表示失败
            raise Exception

    # 线程exit/progress回调：离开主线程队列
    def threadexit(self, myname):
        self.text.insert('end', '%s\text\n' % myname)
        self.text.see('end')

    def threadfail(self, exc_info, myname):
        self.text.insert('end', '%s\tfail\t%s\n' % (myname, exc_info[0]))
        self.text.see('end')

    def threadprogress(self, count, myname):
        self.text.insert('end', '%s\tprogress\t%s\n' % (myname, count))
        self.text.see('end')
        self.text.update()                       # 在这里生效，在主线程中运行

if __name__ == '__main__':
    MyGui().text.mainloop()
