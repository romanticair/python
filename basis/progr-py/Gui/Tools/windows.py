"""
############################################################################
用于封装顶层界面的类。
允许同一个图形界面为主窗口、弹出式窗口或者附加式窗口’内容类可从这些类直接继承，
或者根据使用的模式与这些类混合起来；也可不经过子类直接调用；设计的目的是参照基于
特定应用程序的类进行混合，否则子类从这里（destroy和okayToQuit）获得方法，而不从
基于特定应用程序的类（这些类无法重新定义）。
############################################################################
"""
import os, glob
from tkinter import Tk, Toplevel, Frame, YES, BOTH, RIDGE
from tkinter.messagebox import showinfo, askyesno


class _Window:
    """
    主窗口和弹出式窗口共享mixin
    """
    foundicon = None
    iconpatt = '*.ico'                                          # 所有实例共享
    iconmine = 'py.ico'                                         # 可重置

    def configBorders(self, app, kind, iconfile):
        if not iconfile:                                       # 没有传递图标?
            iconfile = self.findIcon()                          # 尝试当前目录及工具目录
        title = app
        if kind:
            title += ' - ' + kind
        self.title(title)                                       # 窗口边界
        self.iconname(app)                                      # 最小化时
        if iconfile:
            try:
                self.iconbitmap(iconfile)                       # 窗口图标的图像
            except:                                            # python文件或者平台有问题
                pass
        self.protocol('WM_DELETE_WINDOW', self.quit)            # 不自行关闭

    def findIcon(self):
        if _Window.foundicon:                                   # 已经找到图标?
            return _Window.foundicon
        iconfile = None                                         # 先尝试当前目录
        iconshere = glob.glob(self.iconpatt)                     # 只为红色的Tk
        if iconshere:                                           # 指定一个删除图标
            iconfile = iconshere[0]
        else:                                                  # 尝试tools目录下的图标
            mymod = __import__(__name__)                        # 导入self作为目录
            path = __name__.split('.')                          # 指定包路径
            for mod in path[1:]:                               # 循环直到路径末尾
                mymod = getattr(mymod, mod)                     # 仅留下最左边的部分
            mydir = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.iconmine)         # 使用myicon，而不是tk
            if os.path.exists(myicon):
                iconfile = myicon
        _Window.foundicon = iconfile                            # 不再次搜索
        return iconfile


class MainWindow(Tk, _Window):
    """
    当在主要的顶层窗口运行时
    """
    def __init__(self, app, kind='', iconfile=None):
        Tk.__init__(self)
        self._app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):
        if self.okayToQuit():                                  # 线程是否在运行?
            if askyesno(self._app, 'Verify Quit Program?'):
                self.destroy()                                 # 退出整个应用
        else:
            showinfo(self._app, 'Quit not allowed')            # 或者在okayToQuit中?

    def destroy(self):                                       # 自行退出应用程序
        Tk.quit(self)                                          # 如果是退出操作，重新定义

    def okayToQuit(self):                                    # 使用时对此处进行重新定义
        return True                                           # 如线程繁忙时


class PopupWindow(Toplevel, _Window):
    """when run in secondary pop-up window"""
    def __init__(self, app, kind='', iconfile=None):
        Toplevel.__init__(self)
        self._app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):                                          # 对此进行重新定义
        if askyesno(self._app, 'Verify Quit Window?'):
            self.destroy()

    def destroy(self):                                       # 自行关闭窗口
        Toplevel.destroy(self)


class QuietPopupWindow(PopupWindow):
    def quit(self):
        self.destroy()                                        # 不确认关闭


class ComponentWindow(Frame):
    """
    附加到另一个窗口
    """
    def __init__(self, parent):                              # 如果不是一个框架
        Frame.__init__(self, parent)                         # 提供容器
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=RIDGE, border=2)                  # 重新配置

    def quit(self):
        showinfo('Quit', 'Not supported in attachment mode')

    # 从Frame进行销毁：自行擦除框架，针对关闭操作重新定义
