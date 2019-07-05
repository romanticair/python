"""
Python的signal模块演示；传递信号数字作为命令行参数，并用"kill -N pid" shell命令给
该进程发送信号；要保持SIGCHILD处理器有效运行状态；在捕捉之后，所有其它处理器用Python
重置，但是SIGCHLD行为则留给该平台实现，在Windows上，信号也是这样运行，但只定义几个信
号类型；一般来说，信号不具有很好的可移植性。
"""
import sys
import signal
import time


def now():
    return time.asctime()


def onSignal(signum, stackframe):                     # Python signal handler
    print('Got signal', signum, 'at', now())            # most handlers stay in effect
    if signum == signal.SIGCHLD:                        # but sigchld handler is not
        print('sigchld caught')
        # signal.signal(signal.SIGCHLD, onSignal)

signum = int(sys.argv[1])
signal.signal(signum, onSignal)
while True:                                          # install signal handler
    signal.pause()                                     # sleep waiting for signals
