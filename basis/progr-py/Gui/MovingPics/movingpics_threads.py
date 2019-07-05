"""
PyDraw 线程：使用线程来移动对象，Windows系统上正常运行，条件是 canvas.update()
没有被其它线程使用(否则会随着致命错误而退出，一些对象在画出后就开始立即移动等)；
至少一些画布方法调用在 tkinter 中的肯定是安全线程；它不如 time.sleep 平稳，总
之时很危险的，线程是最后的编码，以便更新全局变量，而不改变 GUI。
"""

import sys
import random
import time
import _thread as thread
from tkinter import Tk, mainloop
from movingpics import MovingPics, pickUnits, pickDelays


class MovingPicsThreaded(MovingPics):
    def __init__(self, parent=None):
        MovingPics.__init__(self, parent)
        self.mutex = thread.allocate_lock()
        # sys.setcheckinterval(0) # 在每个 vm 操作后切换：没有帮助

    def onMove(self, event):
        object = self.object
        if object and object not in self.moving:
            msecs = int(pickDelays[0] * 1000)
            parms = 'Delay=%d msec, Units=%d' % (msecs, pickUnits[0])
            self.setTextInfo(parms)
            # self.mutex.acquire()
            self.moving.append(object)
            # self.mutex.release()
            incrX, reptX, incrY, reptY = self.plotMoves(event)
            thread.start_new_thread(self.doMove, (object, event))

    def doMove(self, object, event):
        canvas = event.widget
        incrX, reptX, incrY, reptY = self.plotMoves(event)
        for i in range(reptX):
            canvas.move(object, incrX, 0)
            # canvas.update()
            time.sleep(pickDelays[0])          # 这个可以变更
        for i in range(reptY):
            canvas.move(object, 0, incrY)
            # canvas.update()                  # 更新运行其它应用程序
            time.sleep(pickDelays[0])          # 休眠直至下次移动
        # self.mutex.acquire()
        self.moving.remove(object)
        if self.object == object:
            self.where = event
        # self.mutex.release()

if __name__ == '__main__':
    root = Tk()
    MovingPicsThreaded(root)
    root.mainloop()
