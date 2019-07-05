#!/usr/local/bin/python
"""
##################################################################################
尝试打开任意一个媒体文件。总是使用通用网页浏览器构架，不过也允许使用播放器。
代码不经修改，有可能在系统上无法正常工作；对于音频文件，在Unix下使用filter命令
和命令行打开，在Windows下利用文件名关联通过start命令打开（也就是说，使用机器上的
程序打开.au文件，可能是一个音频播放器，也可能是一个网页浏览器）。可以根据需要进行
配置和扩展。playknownfile假定你知道想打开的文件的媒体类型，而playfile尝试利用Python
mimetypes模块自动决定媒体类型；碰到位置Mimetypes或系统平台时，二者都尝试用Python
webbrowser模块启动一个网页浏览器，作为最后一招
##################################################################################
"""
import os
import sys
import mimetypes
import webbrowser

helpmsg = """
Sorry: can't find a media player for '%s' on your system!
Add an entry for your system to the media player dictionary
for this type of file in playfile.py, or play the file manually.
"""


def trace(*args):
    print(*args)

##################################################################################
# 播放器技巧：通用或特定：待扩展
##################################################################################


class MediaTool:
    def __init__(self, runtext=''):
        self.runtext = runtext

    def run(self, mediafile, **options):             # 多数情况下将忽略options
        fullpath = os.path.abspath(mediafile)         # 当前工作目录可以是任何路径
        self.open(fullpath, **options)


class Filter(MediaTool):
    def open(self, mediafile, **ignored):
        media = open(mediafile, 'rb')
        player = os.popen(self.runtext, 'w')          # 派生shell工具
        player.write(media.read())                    # 发送到它的stdin


class CmdLine(MediaTool):
    def open(self, mediafile, **ignored):            # 运行任何命令行
        cmdLine = self.runtext % mediafile            # 用%s代表文件名
        os.system(cmdLine)


class Winstart(MediaTool):                          # 使用Windows注册表
    def open(self, mediafile, wait=False, **other):
        if not wait:                                 # 也可以使用os.system('start file')
            os.startfile(mediafile)                   # 允许对当前媒体的等待
        else:
            os.system('start /WAIT ' + mediafile)


class Webbrowser(MediaTool):
    def open(self, mediafile, **options):            # file:// 必须用绝对路径
        webbrowser.open_new('file://%s' % mediafile, **options)

##################################################################################
# 媒体类型特异且系统平台特异的策略：修改，或者传入一个新的策略作为代替
##################################################################################

# 建立系统平台和播放器的对应关系：在此修改！

audiotools = {
    'sunos5': Filter('/usr/bin/audioplay'),           # os.popen().write()
    'linux2': CmdLine('cat %s > /dev/audio'),         # 至少在zaurus系统上是这样的
    'sunos4': Filter('usr/demo/SOUND/play'),          # 是的，就是有这么老!
    'win32': Winstart()                               # 用startfile或system打开
    # 'win32': CmdLine('start %s')
}

videotools = {
    'linux2': CmdLine('tkVideo_c700 % s'),            # zaurus pda
    'win32': Winstart()                               # 避免弹出DOS窗口
}

imagetools = {
    'linux2': CmdLine('zimager % s'),                 # zaurus pda
    'win32': Winstart()
}

texttools = {
    'linux2': CmdLine('vi %s'),                       # zaurus pda
    'win32': CmdLine('notepad &s')                    # 后面可以试试PyEdit
}

apptools = {
    'win32': Winstart()                               # doc, xls, 等等：一切风险自行承担
}

# 建立文件名的mimetype与播放器表格的对应关系

mimetable = {'audio': audiotools,
             'video': videotools,
             'image': imagetools,
             'text': texttools,                       # 不是html文本：否则用浏览器
             'application': apptools}

##################################################################################
# 顶层接口
##################################################################################


def trywebbroser(filename, helpmsg=helpmsg, **options):
    """
    用网页浏览器打开文本/html，另外对于其它文件类型，如果碰到未知mimetype
    或系统平台，也用网页浏览器进行尝试，作为最后的办法。
    """
    trace('trying browser', filename)
    try:
        player = Webbrowser()                         # 在本地浏览器打开
        player.run(filename, **options)
    except:
        print(helpmsg % filename)                     # 否则没有能打开的程序


def playknowfile(filename, playertable={}, **options):
    """
    播放类型已知的媒体文件：使用平台特异的播放器对象，如果这个平台下没有相应
    工具则派生一个网页浏览器；接受媒体特异的播放器表格。
    """
    if sys.platform in playertable:
        playertable[sys.platform].run(filename, **options)  # 特殊工具
    else:
        trywebbroser(filename, **options)                   # 通用架构


def playfile(filename, mimetable=mimetable, **options):
    """
    播放类型已知的媒体文件：使用mimetypes猜测媒体类型并对应到平台特异的播放器表格；
    如果是文本/html，或者位置媒体类型，或者没播放器表格，则派生网页浏览器。
    """
    contenttype, encoding = mimetypes.guess_type(filename)   # 检查名称
    if contenttype is None or encoding is not None:       # 无法猜测
        contenttype = '?/?'                                  # 可能是.txt.gz
    maintype, subtype = contenttype.split('/', 1)            # 字符串格式：'图像/jpeg'
    if maintype == 'text' and subtype == 'html':
        trywebbroser(filename, **options)
    elif maintype in mimetable:                            # 尝试使用播放器表格
        playknowfile(filename, mimetable[maintype], **options)
    else:
        trywebbroser(filename, *options)                     # 其它类型

##################################################################################
# 自测代码
##################################################################################
if __name__ == '__main__':
    # 媒体类型已知
    playknowfile('文件.au', audiotools, wait=True)
    playknowfile('文件.gif', imagetools, wait=True)
    playknowfile('文件.jpg', imagetools)

    # 媒体类型猜测完毕
    input('Stop players and press Enter')
    playfile('文件.jpg')                                    # 图像/jpeg
    playfile('文件.gif')                                    # 图像/gif
    playfile('文件1.html')                                  # 文本/html
    playfile('文件2.html')                                  # 文本/html
    playfile('文件.txt')                                    # 文本/纯文本
    playfile('文件.doc')                                    # 程序
    playfile('文件.xls')                                    # 程序
    playfile('文件.au', wait=True)                         # 音频/基本
    input('Done')                                           # 保持打开，单击关闭