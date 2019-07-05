"""
读取一个线程中的命令行管道，将输出放到一个使用计时器循环进行检测的队列中；脚本显
示程序的输出时，输出之间不会发生阻塞；生成的程序不需要连接或刷新，但这却解决了套接
字的复杂性。
"""
import _thread as thread
import queue
import os
from tkinter import Tk
from Gui.Tools.guiStreams import GuiOutput

stdoutQueue = queue.Queue()


def producer(input):
    while True:
        line = input.readline()  # 子线程，如果OK就阻塞
        stdoutQueue.put(line)
        if not line:
            break


def consumer(output, root, term='<end>'):
    try:
        line = stdoutQueue.get(block=False)  # 主线程：检查队列
    except queue.Empty:                      # 4次/秒，如果队列为空则执行此
        pass
    else:
        if not line:                         # 文件末尾终止循环
            output.write(term)                # 否则显示下一行
            return
        output.write(line)
    root.after(250, lambda: consumer(output, root, term))


def redirectedGuiShellCmd(command, root):
    input = os.popen(command, 'r')               # 启动非图形界面程序
    output = GuiOutput(root)
    thread.start_new_thread(producer, (input,))  # 启动读取器线程
    consumer(output, root)

if __name__ == '__main__':
    win = Tk()
    redirectedGuiShellCmd('python -u pipe_nongui.py', win)
    win.mainloop()
