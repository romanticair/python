from tkinter import *


def showPosEvent(event):
    print('Widget=%s X=%s Y=%s' % (event.widget, event.x, event.y))


def showAllEvent(event):
    print(event)
    for attr in dir(event):
        if not attr.startswith('__'):
            print(attr, '=>', getattr(event, attr))


def onKeyPress(event):
    print('Got key press:', event.char)


def onArrowKey(event):
    print('Got up arrow key press')


def onReturnKey(event):
    print('Got return key press')


def onLeftClick(event):
    print('Got left mouse button click:', end='')
    showPosEvent(event)


def onRightClick(event):
    print('Got right mouse button click:', end='')
    showPosEvent(event)


def onMiddleClick(event):
    print('Got middle mouse button click:', end='')
    showPosEvent(event)
    showAllEvent(event)


def onLeftDrag(event):
    print('Got left mouse button drag:', end='')
    showPosEvent(event)


def onDoubleLeftClick(event):
    print('Got double left mouse click', end='')
    showPosEvent(event)
    tkroot.quit()


tkroot = Tk()
labelfont = ('courier', 20, 'bold')                 # 字体系列、大小、字形
widget = Label(tkroot, text='Hello bind world')
widget.config(bg='red', font=labelfont)             # 红色背景，大字体
widget.config(height=5, width=20)                   # 初始大小：行、字符
widget.pack(expand=YES, fill=BOTH)

widget.bind('<Button-1>', onLeftClick)              # 鼠标按钮单击
widget.bind('<Button-3>', onRightClick)
widget.bind('<Button-2>', onMiddleClick)            # 无中间键的可以同时双击代替

widget.bind('<Double-1>', onDoubleLeftClick)        # 双击左键
widget.bind('<B1-Motion>', onLeftDrag)              # 单击右键并拖拉
widget.bind('<KeyPress>', onKeyPress)               # 按下所有键盘键
widget.bind('<Up>', onArrowKey)                     # 按下箭头键
widget.bind('<Return>', onReturnKey)                # 按下返回/回车键
widget.focus()                                      # 或绑定tkroot的按键
tkroot.title('Click me')
tkroot.mainloop()
