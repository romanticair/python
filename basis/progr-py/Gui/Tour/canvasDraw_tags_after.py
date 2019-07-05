"""
相似，但使用widget.after()来安排事件，不再使用time.sleep循环；因为这些是安排的事
件，这就允许椭圆和矩形__same__时间发生移动，而不需要更新调用来刷新屏幕；如果你在
移动过程中按下'o'和'r'，就会发现动作的出现异常：多个移动的更新大约同时开始抖动。
"""

from tkinter import *
import canvasDraw_tags


class CanvasEventsDemo(canvasDraw_tags.CanvasEventsDemo):
    def moveEm(self, tag, moremoves):
        (diffx, diffy), moremoves = moremoves[0], moremoves[1:]
        self.canvas.move(tag, diffx, diffy)
        if moremoves:
            self.canvas.after(250, self.moveEm, tag, moremoves)

    def moveInSquares(self, tag):
        allmoves = [(+20, 0), (0, +20), (-20, 0), (0, -20)] * 5
        self.moveEm(tag, allmoves)

if __name__ == '__main__':
    CanvasEventsDemo()
    mainloop()
