"""
派生FTP get和put GUI, 无论我在哪个目录下运行，os.getcwd不一定是这个脚本的存放目录；
也可以从硬编码路径，或者使用guessLocation；还可以 from launchmodes import PortableLauncher
PortableLauncher('getfilegui', '%s/getfilegui.py' % mydir)()，不过在Windows下需要弹出DOS
控制台来查看已进行的传说的状态信息。
"""
import os
import sys

print('Running in: ', os.getcwd())

# from Launcher import findFirst
# mydir = os.path.split(findFirst(os.curdir, 'PyFtpGui.pyw))[0]

from Tools.find import findlist

mydir = os.path.dirname(findlist('PyFtpGui.pyw', startfir=os.curdir)[0])

if sys.platform[:3] == 'win':
    os.system('start %s\getfilegui.py' % mydir)
    os.system('start %s\putfilegui.py' % mydir)
else:
    os.system('start %s/getfilegui.py' % mydir)
    os.system('start %s/putfilegui.py' % mydir)
