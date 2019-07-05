"""
#######################################################################################
PyView 1.2: 图像幻灯片放映与相关的文字说明

幻灯片放映子类增加笔记文件与一个附加的 PyEdit 对象，一个用于设置幻灯片放映延迟间隔的
比例，和一个标签给当前展示的图像文件命名；

版本 1.2是一个 Python 3.x的断开，但它未隐藏时，也改进了为扩展而重新打包的注释，在一个
子类中捕获注释销毁，以避免关闭弹出窗口或全部组件编辑器时出现的异常，文本插入至最新打包
的注释之前允许 update()，因此将它正确地安置在第一行。
#######################################################################################
"""

import os
from tkinter import *
from Gui.TextEditor.textEditor import *
from slideShow import SlideShow

SIZE = (300, 500)  # 1.2: 此处开始更短(高，宽)


class SlideShowPlus(SlideShow):
    def __init__(self, parent, picdir, editclass, msecs=2000, size=SIZE):
        self.msecs = msecs
        self.editclass = editclass
        SlideShow.__init__(self, parent, picdir, msecs, size)

    def makeWidgets(self):
        self.name = Label(self, text='None', bg='red', relief=RIDGE)
        self.name.pack(fill=X)
        SlideShow.makeWidgets(self)
        Button(self, text='Note', command=self.onNote).pack(fill=X)
        Button(self, text='Help', command=self.onHelp).pack(fill=X)
        s = Scale(label='Speed: msecs delay', command=self.onScale,
                  from_=0, to=3000, resolution=50, showvalue=YES,
                  length=400, tickinterval=250, orient='horizontal')
        s.pack(side=BOTTOM, fill=X)
        s.set(self.msecs)

        # 1.2: 在弹窗或全组件模式中，如果销毁了编辑器则需要知道
        self.editorGone = False

        class WrapEditor(self.editclass):           # 扩展 PyEdit 类至捕获退出
            def onQuit(editor):                      # 编辑器时 PyEdit 实例参数面向对象
                self.editorGone = True                # 在封闭范围中自身是幻灯片放映
                self.editorUp = False
                self.editclass.onQuit(editor)          # 避免递归

        # 附加编辑器框架至窗口或幻灯片放映框架
        if issubclass(WrapEditor, TextEditorMain):     # 现在制造编辑器
            self.editor = WrapEditor(self.master)      # 需要根菜单
        else:
            self.editor = WrapEditor(self)             # 嵌入或弹出
        self.editor.pack_forget()                      # 开始隐藏编辑器
        self.editorUp = self.image = None

    def onStart(self):
        SlideShow.onStart(self)
        self.config(cursor='watch')

    def onStop(self):
        SlideShow.onStop(self)
        self.config(cursor='hand2')

    def onOpen(self):
        SlideShow.onOpen(self)
        if self.image:
            self.name.config(text=os.path.split(self.image[0])[1])
        self.config(cursor='crosshair')
        self.switchNote()

    def quit(self):
        self.saveNote()
        SlideShow.quit(self)

    def drawNext(self):
        SlideShow.drawNext(self)
        if self.image:
            self.name.config(text=os.path.split(self.image[0])[1])
        self.loadNote()

    def onScale(self, value):
        self.msecs = int(value)

    def onNote(self):
        if self.editorGone:              # 已经被销毁
            return                      # 不必重建：假设不需要
        if self.editorUp:
            # self.saveNote()            # 如果编辑器已经打开
            self.editor.pack_forget()    # 保存文件? 隐藏编辑器
            self.editorUp = False
        else:
            # 为再次扩张而重新打包，否则目前不会再扩展
            # 在打包和拆入之间更新，否则首先@ 第二行
            self.editor.pack(side=TOP, expand=YES, fill=BOTH)
            self.editorUp = True        # 否则取消隐藏/打包编辑其实
            self.update()                # 参加 PyEdit: 和 loadFirst 事件一样
            self.loadNote()              # 并且载入图像注释文本

    def switchNote(self):
        if self.editorUp:
            self.saveNote()              # 保存当前图像的注释
            self.loadNote()              # 为新的图像载入注释

    def saveNote(self):
        if self.editorUp:
            currfile = self.editor.getFileName()  # 或 self.editor.onSave()
            currtext = self.editor.getAllText()   # 但文本可能是空的
            if currfile and currtext:
                try:
                    open(currfile, 'w').write(currtext)
                except:
                    pass                         # 如果跑掉一个cd，失败可能是正常的

    def loadNote(self):
        if self.image and self.editorUp:
            root, ext = os.path.splitext(self.image[0])
            notefile = root + '.note'
            self.editor.setFileName(notefile)
            try:
                self.editor.setAllText(open(notefile).read())
            except:
                self.editor.clearAllText()       # 可能没有一个注释

    def onHelp(self):
        showinfo('About PyView', 'PyView version 1.2\nMay, 2018\n(1.1 July 1999)\n'
                                 'An image slide show\nProgramming Python 4th')

if __name__ == '__main__':
    import sys
    picdir = r'../Images/'
    if len(sys.argv) > 1:
        picdir = sys.argv[1]
    editstyle = TextEditorComponentMinimal
    if len(sys.argv) == 3:
        try:
            editstyle = [TextEditorMain,
                         TextEditorMainPopup,
                         TextEditorComponent,
                         TextEditorComponentMinimal][int(sys.argv[2])]
        except:
            pass

    root = Tk()
    root.title('PyView 1.2 - plus text notes')
    Label(root, text='Slide show subclass').pack()
    SlideShowPlus(parent=root, picdir=picdir, editclass=editstyle)
    root.mainloop()
