"""
#####################################################################################
PyClock 2.1: Python/tkinter中的一个时钟 GUI

有着模拟和数字显示模式，一个弹出日期标签，钟面图像，一般调整等。或许都独立运行，或
许嵌入（附加的）其它需要时钟的 GUIs 中运行。

- s/m 键设置秒/分计时器用来弹出消息，窗口图标。
#####################################################################################
"""

import sys
import time
import math
from tkinter import *
from tkinter.simpledialog import askinteger

appname = 'PyClock 2.1'

#####################################################################################
# 选项配置类
#####################################################################################


class ClockConfig:
    # 默认 ---- 在实例或子类重写
    size = 200                                               # 宽度=高度
    bg, fg = 'beige', 'brown'                                # 钟面，滴答颜色
    hh, mh, sh, cog = 'black', 'navy', 'blue', 'red'         # 钟表指针，中心
    picture = None                                          # 钟面照片文件

#####################################################################################
# 数字显示对象
#####################################################################################


class DigitalDisplay(Frame):
    def __init__(self, parent, cfg):
        Frame.__init__(self, parent)
        self.hour = Label(self)
        self.mins = Label(self)
        self.secs = Label(self)
        self.ampm = Label(self)
        for label in self.hour, self.mins, self.secs, self.ampm:
            label.config(bd=4, relief=SUNKEN, bg=cfg.bg, fg=cfg.fg)
            label.pack(side=LEFT)                       # 待定，可扩展，字体规模调整大小

    def onUpdate(self, hour, mins, secs, ampm, cfg):
        mins = str(mins).zfill(2)                       # 或者 '%02d' % x
        self.hour.config(text=str(hour), width=4)
        self.mins.config(text=str(mins), width=4)
        self.secs.config(text=str(secs), width=4)
        self.ampm.config(text=str(ampm), width=4)

    def onResize(self, newWidth, newHeight, cfg):
        pass                                           # 此处没有重画

#####################################################################################
# 模拟显示对象
#####################################################################################


class AnalogDisplay(Canvas):
    def __init__(self, parent, cfg):
        Canvas.__init__(self, parent, width=cfg.size, height=cfg.size, bg=cfg.bg)
        self.drawClockface(cfg)
        self.hourHand = self.minsHand = self.secsHand = self.cog = None

    def drawClockface(self, cfg):                        # 开始并调整大小时
        if cfg.picture:                                     # 绘画椭圆，图画
            try:
                self.image = PhotoImage(file=cfg.picture)   # 背景
            except:
                self.image = BitmapImage(file=cfg.picture)  # 保存参考
            imgx = (cfg.size - self.image.width()) // 2     # 把它集中在一起
            imgy = (cfg.size - self.image.height()) // 2
            self.create_image(imgx+1, imgy+1, anchor=NW, image=self.image)
        originX = originY = radius = cfg.size // 2
        for i in range(60):
            x, y = self.point(i, 60, radius-6, originX, originY)
            self.create_rectangle(x-1, y-1, x+1, y+1, fill=cfg.fg)  # 分钟
        for i in range(12):
            x, y = self.point(i, 12, radius-6, originX, originY)
            self.create_rectangle(x-3, y-3, x+3, y+3, fill=cfg.fg)  # 小时
        self.ampm = self.create_text(3, 3, anchor=NW, fill=cfg.fg)

    def point(self, tick, units, radius, originX, originY):
        angle = tick * (360.0 / units)
        radiansPerDegree = math.pi / 180.0
        pointX = int(round(radius * math.sin(angle * radiansPerDegree)))
        pointY = int(round(radius * math.cos(angle * radiansPerDegree)))
        return pointX + originX + 1, originY + 1 - pointY

    def onUpdate(self, hour, mins, secs, ampm, cfg):      # 回调计时器
        if self.cog:                                       # 重画指针、顿齿
            self.delete(self.cog)
            self.delete(self.hourHand)
            self.delete(self.minsHand)
            self.delete(self.secsHand)
        originX = originY = radius = cfg.size // 2
        hour = hour + (mins / 60.0)
        hx, hy = self.point(hour, 12, radius * .80, originX, originY)
        mx, my = self.point(mins, 60, radius * .90, originX, originY)
        sx, sy = self.point(secs, 60, radius * .96, originX, originY)
        self.hourHand = self.create_line(originX, originY, hx, hy, width=(cfg.size * .04),
                                         arrow='last', arrowshape=(25, 25, 15), fill=cfg.hh)
        self.minsHand = self.create_line(originX, originY, mx, my, width=(cfg.size * .03),
                                         arrow='last', arrowshape=(20, 20, 10), fill=cfg.mh)
        self.secsHand = self.create_line(originX, originY, sx, sy, width=1,
                                         arrow='last', arrowshape=(5, 10, 5), fill=cfg.sh)
        cogsz = cfg.size * .01
        self.cog = self.create_oval(originX-cogsz, originY+cogsz, originX+cogsz, originY-cogsz, fill=cfg.cog)
        self.dchars(self.ampm, 0, END)
        self.insert(self.ampm, END, ampm)

    def onResize(self, newWidth, newHeight, cfg):
        newSize = min(newWidth, newHeight)
        # print('analog onResize', cfg.size+4, newSize)
        if newSize != cfg.size+4:
            cfg.size = newSize-4
            self.delete('all')
            self.drawClockface(cfg)                # 下次调用onUpdate

#####################################################################################
# 时钟复合对象
#####################################################################################

ChecksPerSec = 10                                  # 第二次改变计时器


class Clock(Frame):
    def __init__(self, config=ClockConfig, parent=None):
        Frame.__init__(self, parent)
        self.cfg = config
        self.makeWidgets(parent)                   # 但打包子类
        self.labelOn = 0                           # 打包客户端或坐标方格
        self.display = self.digitalDisplay
        self.lastSec = self.lastMin = -1
        self.countdownSeconds = 0
        self.onSwitchMode(None)
        self.onTimer()

    def makeWidgets(self, parent):
        self.digitalDisplay = DigitalDisplay(self, self.cfg)
        self.analogDispaly = AnalogDisplay(self, self.cfg)
        self.dateLabel = Label(self, bd=3, bg='red', fg='blue')
        parent.bind('<ButtonPress-1>', self.onSwitchMode)
        parent.bind('<ButtonPress-3>', self.onToggleLabel)
        parent.bind('<Configure>', self.onResize)
        parent.bind('<KeyPress-s>', self.onCountdownSec)
        parent.bind('<KeyPress-m>', self.onCountdownMin)

    def onSwitchMode(self, event):
        self.display.pack_forget()
        if self.display == self.analogDispaly:
            self.display = self.digitalDisplay
        else:
            self.display = self.analogDispaly
        self.display.pack(side=TOP, expand=YES, fill=BOTH)

    def onToggleLabel(self, event):
        self.labelOn += 1
        if self.labelOn % 2:
            self.dateLabel.pack(side=BOTTOM, fill=X)
        else:
            self.dateLabel.pack_forget()
        self.update()

    def onResize(self, event):
        if event.widget == self.display:
            self.display.onResize(event.width, event.height, self.cfg)

    def onTimer(self):
        secsSinceEpoch = time.time()
        timeTuple = time.localtime(secsSinceEpoch)
        hour, min, sec = timeTuple[3:6]
        if sec != self.lastSec:
            self.lastSec = sec
            ampm = ((hour >= 12) and 'PM') or 'AM'         # 0...23
            hour = (hour % 12) or 12                        # 12...11
            self.display.onUpdate(hour, min, sec, ampm, self.cfg)
            self.dateLabel.config(text=time.ctime(secsSinceEpoch))
            self.countdownSeconds -= 1
            if self.countdownSeconds == 0:
                self.onCountdownExpire()                    # 倒数计时器
        self.after(1000 // ChecksPerSec, self.onTimer)      # 每秒运行 N 次

    def onCountdownSec(self, event):
        secs = askinteger('Countdown', 'Seconds?')
        if secs:
            self.countdownSeconds = secs

    def onCountdownMin(self, event):
        mins = askinteger('Countdown', 'Minutes?')
        if mins:
            self.countdownSeconds = mins * 60

    def onCountdownExpire(self):
        # 警告：只有一个激活，没有进程指示器
        win = Toplevel()
        msg = Button(win, text='Timer expired', command=win.destroy)
        msg.config(font=('courier', 80, 'normal'), fg='white', bg='navy')
        msg.config(padx=10, pady=10)
        msg.pack(expand=YES, fill=BOTH)
        win.lift()                                          # 增加以上的兄弟姐妹
        if sys.platform[:3] == 'win':                       # Windows 系统上全屏
            win.state('zoomed')

#####################################################################################
# 独立时钟
#####################################################################################

# 使用行的自定义 Tk，顶层的图标等
from Gui.Tools.windows import PopupWindow, MainWindow


class ClockPopup(PopupWindow):
    def __init__(self, config=ClockConfig, name=''):
        PopupWindow.__init__(self, appname, name)
        clock = Clock(config, self)
        clock.pack(expand=YES, fill=BOTH)


class ClockMain(MainWindow):
    def __init__(self, config=ClockConfig, name=''):
        MainWindow.__init__(self, appname, name)
        clock = Clock(config, self)
        clock.pack(expand=YES, fill=BOTH)

# b/w 兼容：手工的窗口边界，传入的父类


class ClockWindow(Clock):
    def __init__(self, config=ClockConfig, parent=None, name=''):
        Clock.__init__(self, config, parent)
        self.pack(expand=YES, fill=BOTH)
        title = appname
        if name:
            title = appname + '-' + name
        self.master.title(title)
        self.master.protocol('WM_DELETE_WINDOW', self.quit)

#####################################################################################
# 程序运行
#####################################################################################

if __name__ == '__main__':
    def getOptions(config, argv):
        for attr in dir(ClockConfig):          # 填充默认的配置对象
            try:                               # 来自 "-attr val" 的命令行参数
                ix = argv.index('-' + attr)     # 跳过_x_间隔
            except:
                continue
            else:
                if ix in range(1, len(argv) - 1):
                    if type(getattr(ClockConfig, attr)) == int:
                        setattr(config, attr, int(argv[ix+1]))
                    else:
                        setattr(config, attr, argv[ix+1])

    # config = PhotoClockConfig()
    config = ClockConfig()
    if len(sys.argv) >= 2:
        getOptions(config, sys.argv)            # clock.py -size -bg 'blue'...
    # myclock = ClockWindow(config, Tk())       # 如果是单独的，父类是 Tk 根
    # myclock = ClockPopup(config, 'popup')
    myclock = ClockMain(config)
    myclock.mainloop()
