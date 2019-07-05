# 预编码时钟的配置风格

from sys import argv
from clock import *
from tkinter import mainloop

gifdir = '../gifs/'


class PPClickSmall(ClockConfig):
    size = 175
    picture = gifdir + '.gif'
    bg, fg, hh, mg = 'white', 'red', 'navy', 'green'


class GilliganClock(ClockConfig):
    size = 500
    picture = gifdir + '.gif'
    bg, fg, hh, mg = 'white', 'red', 'navy', 'yellow'


class LP4EClock(GilliganClock):
    size = 700
    picture = gifdir + '.gif'
    bg = 'navy'


class LP4EClockSmall(LP4EClock):
    size, fg = 350, 'orange'

if __name__ == '__main__':
    if len(argv) > 1:
        gifdir = argv[1] + '/'

    root = Tk()
    for configClass in [ClockConfig, PPClickSmall, LP4EClock, LP4EClockSmall]:
        ClockPopup(configClass, configClass.__name__)
    Button(root, text='Quit Clocks', command=root.quit).pack()
    mainloop()
