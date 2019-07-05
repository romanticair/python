"""
PyDraw后续：简单的画布绘制程序和对象移动器/动画家使用 widget.after 安排事件以实现
对象移动循环，这样可以立即运行不止一个而不会强制使用线程；这会并行移动，但视乎比
time.sleep 版本更慢，请参考 Tour 中的 canvasDraw：创建并立即传递 incX/incY 列表，
在此将会是 allmoves = ([incrX, 0] * reptX) + ([(0, incrY)] * reptY)
"""

from movingpics import *


class MovingPicsAfter(MovingPics):
    def doMoves(self, delay, objectId, incrX, reptX, incrY, reptY):
        if reptX:
            self.canvas.move(objectId, incrX, 0)
            reptX -= 1
        else:
            self.canvas.move(objectId, 0, incrY)
            reptY -= 1
        if not (reptX or reptY):
            self.moving.remove(objectId)
        else:
            self.canvas.after(delay, self.doMoves, delay, objectId, incrX, reptX, incrY, reptY)

    def onMove(self, event):
        traceEvent('onMove', event, 0)
        object = self.object                      # 将 cur 对象移至单击点
        if object:
            msecs = int(pickDelays[0] * 1000)
            parms = 'Delay=%d msec, Units=%d' % (msecs, pickUnits[0])
            self.setTextInfo(parms)
            self.moving.append(object)
            incrX, reptX, incrY, reptY = self.plotMoves(event)
            self.doMoves(msecs, object,  incrX, reptX, incrY, reptY)

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        import movingpics
        movingpics.PicDir = argv[1]
    root = Tk()
    MovingPicsAfter(root)
    root.mainloop()
