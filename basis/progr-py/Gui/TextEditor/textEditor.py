""""
##########################################################################################
PyEdit 2.1: 一个 Python/tkinter 文本文件编辑器和组件


使用 Tk 文本部件，加上 GuiMaker 菜单和工具栏按钮来实现一个功能全面的文本编辑器，这样可以
作为一个独立程序来运行，并且作为一个人组件连接到其它GUIs，它也被 PyMailGUI 和 PyView 用来
编辑邮件文本和图像文本笔记，PyMailGUI 和 PyDemos 用它再弹出模式中展示源文件和文本文件。


2.1版本特征
- Python 3.X 下更新运行
- 增加 "grep" 搜索菜单选项和对话框: 线程外部文件搜索
- 如正在处理的其它编辑窗口有所变动，则在退出应用程序时需进行确认
- 支持用于文件的任意 Unicode 编码: 由 textConfig.py 设置
- 允许一次打开多个字体对话框
- 在新的编辑器中设置文本加载之前允许 self.update()
- 子目录后使用基名来运行代码文件，而不可能是相对路径
- 使用启动模式支持参数用于 Windows 系统上运行编码文件模式

##########################################################################################
"""

Version = '2.1'

import os
import sys
from tkinter import *                                            # 基本构建，常数
from tkinter.colorchooser import askcolor
from tkinter.filedialog import Open, SaveAs                      # 基本对话框
from tkinter.simpledialog import askstring, askinteger
from tkinter.messagebox import showinfo, showerror, askyesno

from Gui.Tools.guimaker import *                                 # 框架 + 菜单/工具栏生成器

helptext = """PyEdit %s Verison

<<Programming Python>> 第四版
Mark Lutz, for O'Reilly Media, Inc.

一个文本编辑程序和可嵌入对象组件都用Python/tkinter编写的，
使用可分离的菜单及工具栏，以便快速使用，还有菜单的Alt快捷键。

%s 版本特色:
- Python 3.X 下运行
- 增加 "grep" 外部文件搜索对话框
- 如其它编辑窗口有所变动，则在退出应用程序时需进行确认
- 支持各文件的任意 Unicode 编码
- 运行多种的变化和多样的字体对话框
- 运行代码选项的多方面改进
- 字体选择对话框
- 无限制撤销/重做
- 只要有变化，退出/打开/新建/运行，都会及时保存
- 搜索区别大小写
- 启动配置模块 textConfig.py
"""

# 常规配置
try:
    import textConfig               # 启动字体和颜色
    configs = textConfig.__dict__    # 如果不在路径或者坏了，照常运行
except:
    configs = {}                     # 在客户端应用程序目录中定义

START = '1.0'                        # 第一个字符的索引: 行=1，列=0
SEL_FIRST = SEL + '.first'           # sel 标签映射到索引
SEL_LAST = SEL + '.last'             # 和 "sel.last" 一样

FontScale = 0                        # Linux系统上使用更大的字体
if sys.platform[:3] != 'win':        # 以及其它非Windows系统的盒子
    FontScale = 3

#######################################################################################
# 主类: 实现编辑器 GUI，行为
# 要求更多特殊的子类混合成特殊风格的 GuiMaker
# 并不是 GuiMaker 的直系子类，因为该类采取多种形式
#######################################################################################


class TextEditor:         # 和菜单/工具栏混合成 Frame 类
    startfiledir = '.'       # 给对话框
    editwindows = []         # 给全过程进行退出检查

    # Unicode 配置
    # 导入到类当中，以便允许子类或自身重写
    if __name__ == '__main__':
        from textConfig import (opensAskUser, opensEncoding,
                                savesUseKnownEncoding, savesAskUser, savesEncoding)
    else:
        from .textConfig import (opensAskUser, opensEncoding,
                                savesUseKnownEncoding, savesAskUser, savesEncoding)

    ftypes = [('All files', '*'),                          # 用于文件打开对话框
              ('Text files', '.txt'),                      # 自定义子类
              ('Python files', '.py')]                     # 或在每个实例中设置

    colors = [{'fg': 'black', 'bg': 'white'},              # 颜色选择列表
              {'fg': 'yellow', 'bg': 'black'},             # 第一项是默认的
              {'fg': 'white', 'bg': 'blue'},               # 根据需要进行调整
              {'fg': 'black', 'bg': 'beige'},              # 或开启 PickBg/Fg 选择器
              {'fg': 'yellow', 'bg': 'purple'},
              {'fg': 'black', 'bg': 'brown'},
              {'fg': 'lightgreen', 'bg': 'darkgreen'},
              {'fg': 'darkblue', 'bg': 'orange'},
              {'fg': 'orange', 'bg': 'darkblue'}]

    fonts = [('courier', 9 + FontScale, 'normal'),         # 与平台无关的字体
             ('courier', 12 + FontScale, 'normal'),        # (字族、大小、字体)
             ('courier', 10 + FontScale, 'bold'),          # 或弹出一个列表框
             ('courier', 10 + FontScale, 'italic'),        # Linux 系统上变得更大
             ('times', 10 + FontScale, 'normal'),          # 给 2 使用 "粗斜体"
             ('helvetica', 10 + FontScale, 'normal'),      # 也有 "下划线" 等
             ('ariel', 10 + FontScale, 'normal'),
             ('system', 10 + FontScale, 'normal'),
             ('courier', 20 + FontScale, 'normal')]

    def __init__(self, loadFirst='', loadEncode=''):
        if not isinstance(self, GuiMaker):
            raise TypeError('TextEditor needs a GuiMaker mixin')
        self.setFileName(None)
        self.lastfind = None
        self.openDialog = None
        self.saveDialog = None
        self.knownEncoding = None                # 2.1 Unicode: 直到打开或保存
        self.text.focus()                        # 否则必须单击文本
        if loadFirst:
            self.update()                        # 2.1: 其它@行2
            self.onOpen(loadFirst, loadEncode)

    def start(self):                                                       # 由GuiMaker.__init__运行
        self.menuBar = [('File', 0, [('Open...', 0, self.onOpen),           # 配置菜单/工具栏
                                     ('Save', 0, self.onSave),              # 一个GuiMaker菜单def树
                                     ('Save As...', 0, self.onSaveAs),      # 给自己內建方法
                                     ('New', 0, self.onNew),                # 标签，快捷方式，回调
                                     'separator',
                                     ('Quit...', 0, self.onQuit)]),
                        ('Edit', 0, [('Undo', 0, self.onUndo),
                                     ('Redo', 0, self.onRedo),
                                     'separator',
                                     ('Cut', 0, self.onCut),
                                     ('Copy', 0, self.onCopy),
                                     ('Paste', 0, self.onPaste),
                                     'separator',
                                     ('Delete', 0, self.onDelete),
                                     ('Select All', 0, self.onSelectAll)]),
                        ('Search', 0, [('Goto...', 0, self.onGoto),
                                       ('Find', 0, self.onFind),
                                       ('Refind', 0, self.onRefind),
                                       ('Change...', 0, self.onChange),
                                       ('Grep...', 0, self.onGrep)]),
                        ('Tools', 0, [('Pick Font...', 0, self.onPickFont),
                                      ('Font List', 0, self.onFontList),
                                      'separator',
                                      ('Pick Bg...', 0, self.onPickBg),
                                      ('Pick Fg...', 0, self.onPickFg),
                                      ('Color List', 0, self.onColorList),
                                      'separator',
                                      ('Info...', 0, self.onInfo),
                                      ('Clone', 0, self.onClone),
                                      ('Run Code', 0, self.onRunCode)])]
        self.toolBar = [('Save', self.onSave, {'side': LEFT}),
                        ('Cut', self.onCut, {'side': LEFT}),
                        ('Copy', self.onCopy, {'side': LEFT}),
                        ('Paste', self.onPaste, {'side': LEFT}),
                        ('Find', self.onRefind, {'side': LEFT}),
                        ('Help', self.help, {'side': RIGHT}),
                        ('Quit', self.onQuit, {'side': RIGHT})]

    def makeWidgets(self):                                  # 由GuiMaker.__init__运行
        name = Label(self, bg='black', fg='white')            # 在下面添加菜单，在上面添加工具
        name.pack(side=TOP, fill=X)                           # 封装菜单/工具栏
        vbar = Scrollbar(self)                                # GuiMaker框架自身就封装好了
        hbar = Scrollbar(self, orient='horizontal')
        text = Text(self, padx=5, wrap='none')                # 禁用自动换行
        text.config(undo=1, autoseparators=1)                 # 默认为0, 1

        vbar.pack(side=RIGHT, fill=Y)
        hbar.pack(side=BOTTOM, fill=X)                        # 最后封装文本
        text.pack(side=TOP, fill=BOTH, expand=YES)            # 否则修剪scrollbars
        text.config(yscrollcommand=vbar.set)                  # 文本移动时调用vbar.set
        text.config(xscrollcommand=hbar.set)
        vbar.config(command=text.yview)                       # 滚动式调用text.yview
        hbar.config(command=text.xview)                       # 或用hbar['command']=text.xview代码

        # 运用用户的配置或默认值
        startfont = configs.get('font', self.fonts[0])
        startbg = configs.get('bg', self.colors[0]['bg'])
        startfg = configs.get('fg', self.colors[0]['fg'])
        text.config(font=startfont, bg=startbg, fg=startfg)
        if 'height' in configs:
            text.config(height=configs['height'])
        if 'width' in configs:
            text.config(width=configs['width'])
        self.text = text
        self.filelabel = name

    ###################################################################################
    # 文件菜单命令
    ###################################################################################

    def my_askopenfilename(self):        # 对象记住最后结果目录/文件
        if not self.openDialog:
            self.openDialog = Open(initialdir=self.startfiledir, filetypes=self.ftypes)
        return self.openDialog.show()

    def my_asksaveasfilename(self):      # 对象记住最后结果目录/文件
        if not self.saveDialog:
            self.saveDialog = SaveAs(initialdir=self.startfiledir, filetypes=self.ftypes)
        return self.saveDialog.show()

    def onOpen(self, loadFirst='', loadEncode=''):
        """
        随着编码传入，文本模式下开启，以textconfig或平台默认值从用户端输入，
        或最后以任意Unicode编码来打开，并终止Windows最后一行上的\r，条件就是
        文本正常显示，读取的内容作为str返回，因此保存时需要编码：保存在此使用
        过的编码。

        提早测试一下文件是否正常以试着避免打开，也可以加载和手动将字节解码为字
        符串，以避免打开多个的尝试，但这样不太可能试用所有情况。

        编码行为在本地的textConfig.py中时可配置的：
        1) 如果由客户端(邮件字符集)传递则优先尝试已知的类型
        2) 如果opensAskUser为真，下一步尝试用户输入(由默认值填充)
        3) 如果opensEncoding非空，下一步尝试这些编码: "latin-1", "cp500" 等
        4) 下一步尝试平台默认的 sys.getdefaultencoding()
        5) 最后使用二进制模式的字节和Tk策略
        """
        if self.text_edit_modified():
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return

        file = loadFirst or self.my_askopenfilename()
        if not file:
            return
        if not os.path.isfile(file):
            showerror('PyEdit', 'Could not open file ' + file)
            return

        # 如果传递过来了且准确无误则尝试已知编码(例如邮件)
        text = None                                       # 空的文件 = '' = 假: 测试 None!
        if loadEncode:
            try:
                text = open(file, 'r', encoding=loadEncode).read()
                self.knownEncoding = loadEncode
            except (UnicodeError, LookupError, IOError):  # 检查: 坏的名字
                pass

        # 尝试用户输入，预设下一个选择为默认值
        if text is None and self.opensAskUser:
            self.update()                                  # 否则在少有的情况下对话框不会出现
            askuser = askstring('PyEdit', 'Enter Unicode encoding for open',
                                initialvalue=(self.opensEncoding or sys.getdefaultencoding() or ''))
            if askuser:
                try:
                    text = open(file, 'r', encoding=askuser).read()
                    self.knownEncoding = askuser
                except (UnicodeError, LookupError, IOError):
                    pass

        # 尝试配置文件(或者在询问用户之前?)
        if text is None and self.opensEncoding:
            try:
                text = open(file, 'r', encoding=self.opensEncoding).read()
                self.knownEncoding = self.opensEncoding
            except (UnicodeError, LookupError, IOError):
                pass

        # 尝试平台默认值(窗口中是utf-8，一直尝试utf-8?)
        if text is None:
            try:
                text = open(file, 'r', encoding=sys.getdefaultencoding()).read()
                self.knownEncoding = sys.getdefaultencoding()
            except (UnicodeError, LookupError, IOError):
                pass

        # 最后一步：使用二进制字节并依赖Tk去解码
        if text is None:
            try:
                text = open(file, 'rb').read()             # 用于Unicode的字节
                text = text.replace(b'\r\n', b'\n')        # 用于显示，保存
                self.knownEncoding = None
            except IOError:
                pass

        if text is None:
            showerror('PyEdit', 'Could not decode and open file ' + file)
        else:
            self.setAllText(text)
            self.setFileName(file)
            self.text.edit_reset()                     # 清除撤销/重做 stks
            self.text.edit_modified(0)                 # 清除修改标志

    def onSave(self):
        self.onSaveAs(self.currfile)                   # 或许为None

    def onSaveAs(self, forcefile=None):
        """
        文本内容中是作为一个字符串返回，因此我们必须处理编码，以便保存到这里的文件，
        而不管输出文件的打开模式(二进制需要字节，而文本必须进行编码)，打开或保存(如
        果已经知晓)时，尝试使用过的编码，用户输入，配置文件设置，最后尝试平台默认值，
        大多数用户都可以使用平台默认值。

        这里保留了成功的编码名以便下次保持，因为这可能是 "新建" 后第一次 "保存" 或是
        手动的文本插入；"保存" 和 "另存为" 可能每个配置文件都使用最后一个已知的编码(它
        可能应该被用于 "保存"，但 "另存为" 的用法尚不清楚)；如果有图形用户界面的提示，
        将其预设为已知的编码。

        手动 text.encode() 来避免创建文件，文本模式的文件执行平台特殊尾行转换：如果打开
        即呈现文本模式(自动)和二进制模式(手动)，那么放弃 Windows \r；如果手动插入内容，
        就必须删除 \r，否则会在此进行复制；如果以二进制打开，则在第一次 "打开" 或 "保存"
        前，"新建" 后将 knownEncoding 置为空(knownEncoding=None)。

        在本地的 textConfig.py中，编码行为是可配置的：
        1) 如果 savesUseKnownEncoding > 0，尝试最后打开或保存的编码
        2) 如果 savesAsUser 为真，下一步尝试用户输入(用已知的?来预先填充)
        3) 如果 savesEncoding 为空，下一步尝试此编码: "utf-8" 等
        4) 最后尝试 sys.getdefaultencoding()
        """
        filename = forcefile or self.my_asksaveasfilename()
        if not filename:
            return
        text = self.getAllText()  # 一个有着\n的str字符串
        encpick = None           # 即便按字节读取/插入

        # 尝试使用最近打开或保存的编码
        if self.knownEncoding and (                                        # 已知编码?
                    (forcefile and self.savesUseKnownEncoding >= 1) or     # 在 "保存" 时?
                    (not forcefile and self.savesUseKnownEncoding >= 2)):  # 在 "另存为" 时?
            try:
                text.encode(self.knownEncoding)
                encpick = self.knownEncoding
            except UnicodeError:
                pass

        # 尝试用户输入，预设为已知的类型，否则下一个选择
        if not encpick and self.savesAskUser:
            self.update()
            askuser = askstring('PyEdit', 'Enter Unicode encoding for save',
                                initialvalue=(self.knownEncoding or self.savesEncoding or
                                              sys.getdefaultencoding() or ''))
            if askuser:
                try:
                    text.encode(askuser)
                    encpick = askuser
                except (UnicodeError, LookupError):                  # LookupError: bad name
                    pass                                             # UnicodeError: can't encode

        # 尝试配置文件
        if not encpick and self.savesEncoding:
            try:
                text.encode(self.savesEncoding)
                encpick = self.savesEncoding
            except (UnicodeError, LookupError):
                pass

        # 尝试默认平台(窗口上是utf-8)
        if not encpick:
            try:
                text.encode(sys.getdefaultencoding())
                encpick = sys.getdefaultencoding()
            except (UnicodeError, LookupError):
                pass

        # 文本模式下打开端线 + 编码
        if not encpick:
            showerror('PyEdit', 'Could not encode for file ' + filename)
        else:
            try:
                file = open(filename, 'w', encoding=encpick)
                file.write(text)
                file.close()
            except:
                showerror('PyEdit', 'Could not write file ' + filename)
            else:
                self.setFileName(filename)    # 或许是新创建的
                self.text.edit_modified(0)    # 清除修改标志
                self.knownEncoding = encpick  # 为下次保存保留编码
                                              # 不要清除撤销/重做 stks!

    def onNew(self):
        """
        在当前窗口从头开始编辑一个新文件，
        请参见 onClone 以弹出一个新的独立的编辑窗口。
        """
        if self.text_edit_modified():
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return self.setFileName(None)
        self.clearAllText()                           # 清除撤销/重做 stks
        self.text.edit_reset()                        # 清除修改标志
        self.knownEncoding = None                    # Unicode 类型未知

    def onQuit(self):
        """
        "退出" 菜单/工具栏上选择并在顶层窗口中 WM 边界的 X 按钮；
        如果其它东西有改动，不退出应用程序；如果自身没有改动则不需询问；最后移至
        顶层窗口类，因为用法各有不同：GUI中的一个 "退出" 可能是使用quit()函数来退
        出，destroy()只有一个顶层，Tk，或编辑框架，作为一个附加组件来运行时或许根
        本没有提供，改进后进行检查，如果使用quit()，主窗口应该检查同在处理列表中的
        其它窗口，以便查看它们是否也有改动。
        """
        assert False, 'onQuit must be defined in window-specific subclass'

    def text_edit_modified(self):
        """
        现在这个正运行！在tkinter中似乎一直有个bool结果类型；
        """
        # 返回 self.tk.call((self.text._w, 'edit') + ('modified', None))
        return self.text.edit_modified()

    ####################################################################################
    # 编辑菜单命令
    ####################################################################################

    def onUndo(self):
        try:                                          # tk8.4 保留撤销/重做堆栈
            self.text.edit_undo()                     # 堆栈为空则抛出异常
        except TclError:                             # 可分离的菜单供快速撤销使用
            showinfo('PyEdit', 'Nothing to undo')

    def onRedo(self):
        try:
            self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')

    def onCopy(self):                                # 使用鼠标选中文本等
        if not self.text.tag_ranges(SEL):            # 保存进跨应用程序的剪贴板
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onDelete(self):                             # 删除选中的文本，不保存
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.onCopy()                            # 保存并删除选中的文本
            self.onDelete()

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('PyEdit', 'Nothing to paste')
            return
        self.text.insert(INSERT, text)               # 增加当前嵌入的光标
        self.text.tag_remove(SEL, '1.0', END)
        self.text.tag_add(SEL, INSERT + '-%dc' % len(text), INSERT)
        self.text.see(INSERT)                        # 选择它，因此它可以被削减

    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END + '-1c')   # 选择整个文本
        self.text.mark_set(INSERT, '1.0')            # 移动插入点至顶部
        self.text.see(INSERT)                        # 滚动至顶部

    ####################################################################################
    # 搜索菜单命令
    ####################################################################################

    def onGoto(self, forceline=None):
        line = forceline or askinteger('PyEdit', 'Enter line number')
        self.text.update()
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END + '-1c')
            maxline = int(maxindex.split('.')[0])
            if 0 < line <= maxline:
                self.text.mark_set(INSERT, '%d.0' % line)      # 转到行
                self.text.tag_remove(SEL, '1.0', END)          # 删除选择
                self.text.tag_add(SEL, INSERT, 'insert + 1l')  # 选择行
                self.text.see(INSERT)                          # 滚至行
            else:
                showerror('PyEdit', 'Bad line number')

    def onFind(self, lastkey=None):
        key = lastkey or askstring('PyEdit', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind = key
        if key:
            nocase = configs.get('caseinsens', True)         # 不区分大小写
            where = self.text.search(key, INSERT, END, nocase=nocase)
            if not where:
                showerror('PyEdit', 'String not found')       # 不要换行
            else:
                pastkey = where + '+%dc' % len(key)           # 索引过去的键
                self.text.tag_remove(SEL, '1.0', END)         # 移除任何 sel
                self.text.tag_add(SEL, where, pastkey)        # 选择键
                self.text.mark_set(INSERT, pastkey)           # 为了下一次查找
                self.text.see(where)                          # 滚动显示

    def onRefind(self):
        self.onFind(self.lastfind)

    def onChange(self):
        """
        非模态查找/变换对话框；
        将每个对话框的输入传递给回调函数，也许 > 1 变换对话框会打开。
        """
        new = Toplevel(self)
        new.title('PyEdit - change')
        Label(new, text='Find text?', relief=RIDGE, width=15).grid(row=0, column=0)
        Label(new, text='Change to?', relief=RIDGE, width=15).grid(row=1, column=0)
        entry1 = Entry(new)
        entry2 = Entry(new)
        entry1.grid(row=0, column=1, sticky=EW)
        entry2.grid(row=1, column=1, sticky=EW)

        def onFind():                    # 封闭范围中使用我的条目
            self.onFind(entry1.get())     # 运行正常查找对话框回调函数

        def onApply():
            self.onDoChange(entry1.get(), entry2.get())

        Button(new, text='Find', command=onFind).grid(row=0, column=2, sticky=EW)
        Button(new, text='Apply', command=onApply).grid(row=1, column=2, sticky=EW)
        new.columnconfigure(1, weight=1)  # 扩展项目

    def onDoChange(self, findtext, changeto):
        # 变换对话框中使用 "应用"：变换和重查找
        if self.text.tag_ranges(SEL):           # 必须先寻找
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.text.insert(INSERT, changeto)  # 为空则删除
            self.text.see(INSERT)
            self.onFind(findtext)               # 跳转到下一个出现的地方
            self.text.update()                  # 强制刷新

    def onGrep(self):
        """
        线程外部文件搜索；在目录树中以字符串来搜索匹配的文件名；在出现的行单击列表框
        打开相匹配的文件；

        搜索是线程的，因此 GUI 仍然活跃并且不堵塞，以便允许多个 grep 及时的重叠；可以
        使用线程工具，但要避免不活的 grep 中的循环；

        grep Unicode 策略：搜索树中文本文件的内容可能是任意的Unicode编码，在这里只打开，
        但允许此编码用于整个树的输入，将它预设为平台文件系统或默认的文本，并跳过编码失败
        的文件，最坏的情况是如果有几率存在N种编码，用户可能需要允许 N 次grep；否则打开可
        能会引发异常，在二进制模式下打开可能无法将编码文本域搜索字符相匹配；

        待定：如果任何文件都解码失败，更好的发现错误？但在 "记事本" 中创建的 utf-16 2个
        字节/字符格式可能经 utf-8 解码而不会有错误，搜索字符串不会被发现；
        待定：可能运行多种编码名称的输入，用逗号分开，每个文件尝试一种编码，不需要打开
        loadEncode?
        """
        from Gui.ShellGui.formrows import makeFormRow

        # 非模态的对话框(get dirname, filenamepatt, grepkey)
        popup = Toplevel()
        popup.title('PyEdit - grep')
        var1 = makeFormRow(popup, label='Directory', width=18, browse=False)
        var2 = makeFormRow(popup, label='Filename pattern', width=18, browse=False)
        var3 = makeFormRow(popup, label='Search string', width=18, browse=False)
        var4 = makeFormRow(popup, label='Content encoding', width=18, browse=False)
        var1.set('.')                                  # 当前目录
        var2.set('*.py')                               # 初始值
        var4.set(sys.getdefaultencoding())             # 用于文件内容，而非文件名
        cb = lambda: self.onDoGrep(var1.get(), var2.get(), var3.get(), var4.get())
        Button(popup, text='Go', command=cb).pack()

    def onDoGrep(self, dirname, filenamepatt, grepkey, encoding):
        """
        跳至 grep 对话框：填充匹配的滚动列表
        待定：发生器线程应该守护进程吗，这样它会与应用程序一起终止?
        """
        import threading
        import queue

        # 制作非模态不可关闭的对话框
        mypopup = Tk()
        mypopup.title('PyEdit - grepping')
        status = Label(mypopup, text='Grep thread searching for: %r...' % grepkey)
        status.pack(padx=20, pady=20)
        mypopup.protocol('WM_DELETE_WINDOW', lambda: None)  # ignore X close
        # 启动发生器线程，消费器循环
        myqueue = queue.Queue()
        threadargs = (filenamepatt, dirname, grepkey, encoding, myqueue)
        threading.Thread(target=self.grepThreadProducer, args=threadargs).start()
        self.grepThreadConsumer(grepkey, encoding, myqueue, mypopup)

    def grepThreadProducer(self, filenamepatt, dirname, grepkey, encoding, myqueue):
        """
        在一个非 GUI 的并列线程：使find.find结果列表排序；
        也可以将查找的匹配项排序，但需要保留窗口；
        文件内容和文件名称在这可能都无法解码；

        待定：可以通过解码字节来查找以避免os.walk/listdir中文件名解码异常，
        但使用哪个编码? sys.getfilesystemcoding()如果不为空呢?
        """
        from Tools.find import find
        matches = []
        try:
            for filepath in find(pattern=filenamepatt, startdir=dirname):
                try:
                    textfile = open(filepath, encoding=encoding)
                    for (linenum, linestr) in enumerate(textfile):
                        if grepkey in linestr:
                            msg = '%s@%d [%s]' % (filepath, linenum + 1, linestr)
                            matches.append(msg)
                except UnicodeError as x:
                    print('Unicode error in:', filepath, x)  # 例如：解码，bom
                except IOError as x:
                    print('IO error in:', filepath, x)       # 例如：许可
        finally:
            myqueue.put(matches)                              # 发现异常就停止消费器循环: 文件名?

    def grepThreadConsumer(self, grepkey, encoding, myqueue, mypopup):
        """
        在主 GUI 线程：观察结果队列或[]；可能有许多活跃的 grep 线程/循环/队列；
        可能还有其它线程类型/进行中的检查器，尤其是 PyEdit 作为附加组件时(PyMailGUI)；
        """
        import queue
        try:
            matches = myqueue.get(block=False)
        except queue.Empty:
            myargs = (grepkey, encoding, myqueue, mypopup)
            self.after(250, self.grepThreadConsumer, *myargs)
        else:
            mypopup.destroy()       # 关闭状态
            self.update()           # 现在就删除它
            if not matches:
                showinfo('PyEdit', 'Grep found no matches for: %r' % grepkey)
            else:
                self.grepMatchesList(matches, grepkey, encoding)

    def grepMatchesList(self, matches, grepkey, encoding):
        """
        成功匹配后填充列表；
        从搜索中我们已经知道 Unicode 编码；
        单击文件名时在这使用它，因此打开不询问用户。
        """
        from Gui.Tour.scrolledlist import ScrolledList

        print('Matches for %s: %s' % (grepkey, len(matches)))

        # 双击捕获列表文件并打开
        class ScrolledFilenames(ScrolledList):
            def runCommand(self, selection):
                file, line = selection.split('[', 1)[0].split('@')
                editor = TextEditorMainPopup(loadFirst=file, winTitle='grep match', loadEncode=encoding)
                editor.onGoto(int(line))
                editor.text.focus_force()  # no, really

        # 信件非模态窗口
        popup = Tk()
        popup.title('PyEdit - grep matches: %r (%s)' % (grepkey, encoding))
        ScrolledFilenames(parent=popup, options=matches)

    ##############################################################################################
    # 工具菜单命令
    ##############################################################################################

    def onFontList(self):
        self.fonts.append(self.fonts[0])            # 在列表中挑选下一个字体
        self.fonts.remove(self.fonts[0])            # 调整文本区域的大小
        self.text.config(font=self.fonts[0])

    def onColorList(self):
        self.colors.append(self.colors[0])          # 在列表中挑选下一种颜色
        self.colors.remove(self.colors[0])          # 移动目前的至结尾
        self.text.config(fg=self.colors[0]['fg'], bg=self.colors[0]['bg'])

    def onPickFg(self):
        self.pickColor('fg')    # 加入10/02/00

    def onPickBg(self):       # 挑选任意的颜色
        self.pickColor('bg')    # 在标准颜色对话框中

    def pickColor(self, part):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(**{part: hexstr})

    def onInfo(self):
        """
        弹出对话框给出文字统计和光标位置。
        警告：Tk插入位置的列将制表符作为一个字符：转换成 8倍 以匹配视觉吗?
        """
        text = self.getAllText()             # 15 分钟内加入 5/3/00
        tbytes = len(text)                   # 使用一个简单的猜测
        lines = len(text.split('\n'))        # 通过空白字符进行分割
        words = len(text.split())            # 3.X：字节实际上是字符
        index = self.text.index(INSERT)      # 字符串是 unicode 编码点
        where = tuple(index.split('.'))
        showinfo('PyEdit Information', 'Current location:\n\n' +
                 'line:\t%s\ncolumn:\t%s\n\n' % where +
                 'File text statistics:\n\n' +
                 'chars:\t%d\nlines:\t%d\nwords:\t%d\n' % (tbytes, lines, words))

    def onClone(self, makewindow=True):
        """
        打开一个新的编辑窗口，而不是改变一个已经打开的(onNew)；
        继承了退出，克隆窗口的其他行为；
        如果让它自己弹出，子类必须重新定义/代替这个类，否则这个
        类会在此创建一个假的额外的窗口，这个窗口时空的。
        """
        if not makewindow:
            new = None                      # 假设类成为了自己的窗口
        else:
            new = Toplevel()                 # 同一过程中的编辑窗口
        myclass = self.__class__             # 实例的(最低)类对象
        myclass(new)                         # 连接/运行我的类的实例

    def onRunCode(self, parallelmode=True):
        """
        运行正在编辑的代码 ---- 不是一个IDE，却很方便；尝试在文件目录下运行，而不是 cwd，
        为脚本文件输入并添加命令行参数；

        编码的标准输入/输出/错误 = 编辑器的启动窗口，如有的话：运行一个控制台窗口以看到代
        码的打印输出；但并行模式使用开始去给输入/输出打开一个DOS窗口；模块搜索路径将包括
        '.' 目录，那是开始的地方；
        在非文件模式，编码的 Tk 根可能是PyEdit的窗口。子过程或多重处理模块可能也在此运行；

        在子目录后固定使用基文件名，而非路径后；
        使用StartArgs来容许Windows系统文件模式中的参数；
        在第一次对话后运行一个update()，否则少数情况下第二对话有时不会出现；
        """
        from launchmodes import System, Start, StartArgs, Fork

        def askcmdargs():
            return askstring('PyEdit', 'Commandline arguments?') or ''

        filemode = False
        thefile = str(self.getFileName())
        if os.path.exists(thefile):
            filemode = askyesno('PyEdit', 'Run from file?')
            self.update()                                       # 运行update()
        if not filemode:                                       # 运行文本字符串
            cmdargs = askcmdargs()
            namespace = {'__name__': '__main__'}                # 作为顶层运行
            sys.argv = [thefile] + cmdargs.split()              # 可以使用线程
            exec(self.getAllText() + '\n', namespace)           # 忽略异常
        elif self.text_edit_modified():                        # 已变的测试
            showerror('PyEdit', 'Text changed: you must save before run')
        else:
            cmdargs = askcmdargs()
            mycwd = os.getcwd()                                 # cwd 可能是根
            dirname, filename = os.path.split(thefile)          # 得到目录，基
            os.chdir(dirname or mycwd)                          # 对于文件名 cd
            thecmd = filename + ' ' + cmdargs                   # 不是这个文件
            if not parallelmode:                               # 作为文件运行
                System(thecmd, thecmd)()                        # 阻塞编辑器
            else:
                if sys.platform[:3] == 'win':                   # 并行生产
                    run = StartArgs if cmdargs else Start      # 支持参数
                    run(thecmd, thecmd)()                       # 或者一直生产
                else:
                    Fork(thecmd, thecmd)()                      # 并行生产
            os.chdir(mycwd)                                     # 返回我的目录

    def onPickFont(self):
        """
        每个对话框的输入传递至回调函数，或许 > 1 字体对话框打开
        """
        from Gui.ShellGui.formrows import makeFormRow
        popup = Toplevel(self)
        popup.title('PyEdit - font')
        var1 = makeFormRow(popup, label='Family', browse=False)
        var2 = makeFormRow(popup, label='Size', browse=False)
        var3 = makeFormRow(popup, label='Style', browse=False)
        var2.set('12')                        # 建议的 vals
        var3.set('bold italic')               # 参加选择列表用于有效输入
        Button(popup, text='Apply', command=lambda: self.onDoFont(var1.get(), var2.get(),
                                                                  var3.get())).pack()

    def onDoFont(self, family, size, style):
        try:
            self.text.config(font=(family, int(size), style))
        except:
            showerror('PyEdit', 'Bar font sepecification')

    ##################################################################################
    # 实用程序，此类之外的用处
    ##################################################################################

    def isEmpty(self):
        return not self.getAllText()

    def getAllText(self):
        return self.text.get('1.0', END + '-1c')        # 作为 str 字符串抽取文本

    def setAllText(self, text):
        """
        调用程序：如果恰好已封装则首先调用 self.update()，否则初始位置可能会在第2行，
        而不是第一行(Tk的错误?)。
        """
        self.text.delete('1.0', END)                     # 在小部件中存储文本字符串
        self.text.insert(END, text)                      # 或'1.0'，文本=字节或字符串
        self.text.mark_set(INSERT, '1.0')                # 将插入点移至顶部
        self.text.see(INSERT)                            # 滚至顶部，插入集

    def clearAllText(self):
        self.text.delete('1.0', END)                     # 在小部件中清楚文本

    def getFileName(self):
        return self.currfile

    def setFileName(self, name):                       # 请参阅 onGoto(linenum)
        self.currfile = name                             # 用于保存
        self.filelabel.config(text=str(name))

    def setKnowEncoding(self, encoding='utf-8'):      # 如果插入则用于保存
        self.knownEncoding = encoding                    # 否则保存使用配置，询问?

    def setBg(self, color):
        self.text.config(bg=color)                       # 从代码 def 手动设置

    def setFg(self, color):
        self.text.config(fg=color)                       # "黑"， 十六进制串

    def setFont(self, font):
        self.text.config(font=font)                      # ("字族", 大小, "风格")

    def setHeight(self, lines):                        # 默认= 24h x 80w
        self.text.config(height=lines)                   # 也可能来自于 textConfig.py

    def setWidth(self, chars):
        self.text.config(width=chars)

    def clearModified(self):
        self.text.edit_modified(0)                      # 清楚修改的标记

    def isModified(self):
        return self.text_edit_modified()               # 从上次重设开始改变?

    def help(self):
        showinfo('About PyEdit', helptext % ((Version,) * 2))

################################################################################
# 准备使用的编辑器类
# 混合在一个 GuiMaker 框架子类，这个子类创建菜单和工具栏
#
# 这些类是常见的用例，但其它配置都是可能的；
# 调用 TextEditorMain().mainloop() 以开启 PyEdit() 作为一个独立的程序；
# 在一个子类中重新定义/扩展 onQuit 来捕获退出或销毁(参加 PyView)；
# 警告：可以给图标使用 windows.py 但退出协议在这是定制的。
################################################################################

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 退出时，如果进程中没有其他更改过的编辑窗口正打开，那就不要默默地退出整个应用程序 ---- 更改
# 的东西可能丢失，因为所有其它窗口也都关闭，包括多个 Tk 编辑器的父类；使用一个列表来跟踪所有
# 进程中打开的 PyEdit 窗口实例；这可能太宽了(如果我们使用 destroy() 代替 quit()，就只需要检查
# 被销毁父类的子类)，不过最好还是宁可失之过于包容；onQuit 移至此处因为每个窗口类型各有不同，
# 尽管不是呈现的；

# 假设一个 TextEditorMainPopup 从来都不是其他编辑窗口的一个父类 ---- 顶层的子类随他们的父类一
# 起被销毁了，这里并没有寻址此处 PyEdit 类范围之外的关闭(tkinter可在每个部件退出，而任何部件类
# 型可能是一个顶层的父类!)；客户端负责检查所有涵盖情况中编辑器内容的变化；

# 注意：tkinter的 <Destroy> 绑定事件再此处不好有帮助，因为它的回调不能允许 GUI 的操作。
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

################################################################################
# 当文本编辑器拥有窗口
################################################################################


class TextEditorMain(TextEditor, GuiMakerWindowMenu):
    """
    PyEdit 主窗口用 quit() 在GUI中的 "退出" 键来退出应用程序，并且在窗口上建立一个菜单；
    父类可能是默认的 Tk，显式的Tk，或顶层的：父类肯定是一个窗口，可能是一个Tk，因此它不
    是默默的被销毁，和父类一同关闭；所有 PyEdit 主窗口检查所有 PyEdit 其它在进程中开启的
    窗口来更改 GUI 中的 "退出"键，因为这里的一个 quit() 将会退出整个应用程序；编辑器的框
    架不必占据整个窗口(可能还有其它部分：参加 PyView)，但它的 "退出" 终止程序；onQuit 是
    在工具栏或文件菜单、以及窗口边框 X 中运行退出；
    """
    def __init__(self, parent=None, loadFirst='', loadEncode=''):
        # 编辑器填充整个父类窗口
        GuiMaker.__init__(self, parent)                       # 使用主窗口菜单
        TextEditor.__init__(self, loadFirst, loadEncode)      # GuiMaker 框架自我包装
        self.master.title('PyEdit ' + Version)
        self.master.iconname('PyEdit')
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)
        TextEditor.editwindows.append(self)

    def onQuit(self):                                       # GUI 关闭中的退出请求
        close = not self.text_edit_modified()                # 自我检查，询问? 检查，其它
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            windows = TextEditor.editwindows
            changed = [w for w in windows if w != self and w.text_edit_modified()]
            if not changed:
                GuiMaker.quit(self)                          # 退出末端所有的应用程序而不管部件类型
            else:
                numchange = len(changed)
                verify = '%s other edit window%s changed: quit and discard anyhow?'
                verify = verify % (numchange, 's' if numchange > 1 else '')
                if askyesno('PyEdit', verify):
                    GuiMaker.quit(self)


class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    """
    弹出的 PyEdit 窗口 destroy() 以在GUI中的 "退出" 键关闭自身，并在窗口上创建一个菜单；
    制造顶层自己的父类，这是默认 Tk(为空)的子类或其它置为传入的窗口或部件(例如：一个框架)；
    如果任何 PyEdit 主窗口都退出则退出则增加到列表，因此将会对更改进行检查；如果任何 PyEdit
    主窗口将被创建，它的父类应该也是一个 PyEdit 主窗口的父类，因此它在被追踪时不会默默的关
    闭；onQuit 是在工具栏或文件菜单、以及窗口边框 X 中运行退出；
    """
    def __init__(self, parent=None, loadFirst='', winTitle='', loadEncode=''):
        # 创建自己的窗口
        self.popup = Toplevel(parent)
        GuiMaker.__init__(self, self.popup)                  # 使用主窗口菜单
        TextEditor.__init__(self, loadFirst, loadEncode)     # 新弹窗中的框架
        assert self.master == self.popup
        self.popup.title('PyEdit ' + Version + winTitle)
        self.popup.iconname('PyEdit')
        self.popup.protocol('WM_DELETE_WINDOW', self.onQuit)
        TextEditor.editwindows.append(self)

    def onQuit(self):
        close = not self.text_edit_modified()
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            self.popup.destroy()                             # 只终止这个窗口
            TextEditor.editwindows.remove(self)              # (加上任何子窗口)

    def onClone(self):
        TextEditor.onClone(self, makewindow=False)          # 制造我自己的弹窗

##########################################################################################
# 当编辑器嵌入另一个窗口
##########################################################################################


class TextEditorComponent(TextEditor, GuiMakerFrameMenu):
    """
    附加的 PyEdit 组件框架支持完整的菜单/工具栏选项，它再GUI中的退出运行一个 destroy()，
    只用来清除自身；在GUI中的退出在此验证自身是否有任何改变；不拦截窗口管理器边框 X：
    不拥有窗口，不会把自身添加到更改追踪列表：作为较大的应用程序的一部分；
    """
    def __init__(self, parent=None, loadFirst='', winTitle='', loadEncode=''):
        # 使用基于框架的菜单
        GuiMaker.__init__(self, self.popup)                  # 所有菜单，按键打开
        TextEditor.__init__(self, loadFirst, loadEncode)     # GuiMaker 必须初始化

    def onQuit(self):
        close = not self.text_edit_modified()
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            self.destroy()                                  # 我、清除本身框架但不会退出封闭的应用程序


class TextEditorComponentMinimal(TextEditor, GuiMakerFrameMenu):
    """
    附加的 PyEdit 组件框架不支持 "退出" 和 "文件" 菜单选项，在启动时，从工具栏移除
    "退出"，要么删除 "文件" 菜单，要么禁止所有它的项目(可能是独创性的，但足够了)；
    菜单和工具栏的结构是每个实例数据：更改不影响其他；在GUI中的退出来永远不会发生，
    因为可用选项中删除了它；
    """
    def __init__(self, parent=None, loadFirst='', deleteFile=True, loadEncode=''):
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)                      # GuiMaker 框架自身包容
        TextEditor.__init__(self, loadFirst, loadEncode)     # TextEditor 增加中间

    def start(self):
        TextEditor.start(self)                               # GuiMaker开始调用
        for i in range(len(self.toolBar)):                  # 在工具栏中删除退出
            if self.toolBar[i][0] == 'Quit':                 # 删除文件菜单项目，
                del self.toolBar[i]                          # 或只禁用文件
                break
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]
                    break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':
                    items.append([1, 2, 3, 4, 6])

##########################################################################################
# 运行独立程序
##########################################################################################


def testPopup():
    # 参加PyView 和 PyMail 用于组件测试
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()


def main():                       # 或许是被键入或单击
    try:                           # 或在 Windows 上联合
        fname = sys.argv[1]        # 参数 = 可选的文件名
    except IndexError:            # 创建进默认的 Tk 根
        fname = None
    TextEditorMain(loadFirst=fname).pack(expand=YES, fill=BOTH)  # 包容可选
    mainloop()

if __name__ == '__main__':         # 作为一个脚本运行时
    testPopup()
    # main()                       # 为无 DOS 窗口运行 .pyw
