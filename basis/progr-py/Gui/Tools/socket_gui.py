# 图形用户界面服务器：读取并显示非图形用户界面脚本的输出

import sys
import os                              # 包括error
from socket import *
from tkinter import Tk
from launchmodes import PortableLauncher
from Gui.Tools.guiStreams import GuiOutput

myport = 50008
sockobj = socket(AF_INET, SOCK_STREAM)  # 图形用户界面充当服务器，脚本充当客户端
sockobj.bind(('', myport))              # 先配置服务器，再配置客户端
sockobj.listen(5)

print('starting')
PortableLauncher('nongui', 'socket_nongui.py -gui')()  # 生成非图形用户界面脚本

print('acception')
conn, addr = sockobj.accept()  # 等待客户端连接
conn.setblocking(False)       # 使用非阻塞套接字(False=0)
print('accepted')


def checkdata():
    try:
        message = conn.recv(1024)       # 不要阻塞
        # output.write(message + '\n')  # 因为输入也能实现sys.stdout=output
        print(message, file=output)     # 如果就绪，在图形界面窗口中显示文本
    except error:
        print('no data')                # 打印到sys.stdout
    root.after(1000, checkdata)

root = Tk()
output = GuiOutput(root)                # 显示套接字文本
checkdata()
root.mainloop()
