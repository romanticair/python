"""
######################################################################################
用命令行和可复用的启动方案类来启动Python程序；在命令行开头自动向Python可执行文件插入
"Python"和/或路径；这个模块的某些部分可能假定"python"在你的系统路径中(参考Launcher.py)

使用subprocess模块也可行，不过os.popen()在内部调用这个模块，目标是在这里启动一个独立运行的
程序，而非连接到它的流；multiprocessing模块也是一个选择，不过这里处理命令行而非函数，为实
现这里的选项之一而开始一个进程不是很合理；

这一版的更新：脚本文件名路径将经过normpath()处理，必要时将所有/改成\以供Windows工具使用；
PyEdit和其它工具继承这个修改，在Windows下，一般允许在文件中用/，但并非所有启动工具；
######################################################################################
"""

import sys
import os

pyfile = (sys.platform[:3] == 'win' and 'python.exe') or 'python'
pypath = sys.executable


def fix_windows_path(cmdline):
    """
    将cmdline开头的脚本文件名路径里所有的/改成\；在Windows下，仅为运行需要这种处理的
    工具的类所使用；在其它平台上，这么做也没有坏处(如Unix下的os.system)。
    """
    splitline = cmdline.strip().split(' ')             # 在空格处分割字符串
    fixedpath = os.path.normpath(splitline[0])         # 解决斜杠的问题
    return ' '.join([fixedpath] + splitline[1:])      # 把路径重新拼起来


class LaunchMode:
    """
    在实例中待命，声明标签并运行命令；子类按照run()中的需要格式化命令行；命令
    应当以准备运行的Python脚本名开头，而且不带"python"或脚本的完整路径；
    """
    def __init__(self, label, command):
        self.what = label
        self.where = command

    def __call__(self, *args, **kwargs):       # 等待调用，执行按钮按下的回调动作
        self.announce(self.what)
        self.run(self.where)                    # 子类必须定义run()

    def announce(self, text):                 # 子类可以重新定义announnce()
        print(text)

    def run(self):
        assert False, 'run must be defined'


class System(LaunchMode):
    """
    运行shell命令行中指定的Python脚本，小心：可能阻塞调用者，除非在
    Unix下带上&操作符
    """
    def run(self, cmdline):
        cmdline = fix_windows_path(cmdline)
        os.system('%s %s' % (pypath, cmdline))


class Popen(LaunchMode):
    """
    在新进程中运行shell命令行；小心：可能阻塞调用者，因为管道关闭得太快
    """
    def run(self, cmdline):
        cmdline = fix_windows_path(cmdline)
        os.popen(pypath + ' ' + cmdline)


class Fork(LaunchMode):
    """
    显示地创建新进程中运行命令，仅在类Unix系统下可用，包括Cygwin
    """
    def run(self, cmdline):
        assert hasattr(os, 'fork')
        cmdline = cmdline.split()                     # 把字符串转换成列表
        if os.fork() == 0:                            # 开始行的子进程
            os.execvp(pypath, [pyfile] + cmdline)     # 在子进程中运行新程序


class Start(LaunchMode):
    """
    独立于调用者运行程序；仅在Windows下可以：使用了文件名关联
    """
    def run(self, cmdline):
        assert sys.platform[:3] == 'win'
        cmdline = fix_windows_path(cmdline)
        os.startfile(cmdline)


class StartArgs(LaunchMode):
    """
    仅在Windows下可用：args可能需要用到真正的start命令：斜杠在这里没问题
    """
    def run(self, cmdline):
        assert sys.platform[:3] == 'win'
        os.system('start ' + cmdline)


class Spawn(LaunchMode):
    """
    在独立于调用者的新进程中运行Python；在Windows下和Unix下都可用；
    DOS使用P_NOWAIT；斜杠在这里没问题
    """
    def run(self, cmdline):
        os.spawnv(os.P_DETACH, pypath, (pyfile, cmdline))


class TopLevel(LaunchMode):
    """
    在新窗口中运行，进程是同一个，待讨论：还需要GUI类信息
    """
    def run(self, cmdline):
        assert False, 'Sorry - mode not yet inplemented'

#
# 为这个平台挑选一个"最佳"启动器
# 可能需要在其它地方细化这个选项
#

if sys.platform[:3] == 'win':
    PortableLauncher = Spawn
else:
    PortableLauncher = Fork


class QuietPortableLauncher(PortableLauncher):
    def announce(self, text):
        pass


def self_test():
    file = 'echo.py'
    input('default mode...')
    launcher = PortableLauncher(file, file)
    launcher()                               # 不阻塞

    input('system mode...')
    System(file, file)()                     # 阻塞

    if sys.platform[:3] == 'win':
        input('DOS start mode...')
        StartArgs(file, file)()

if __name__ == '__main__':
    self_test()
