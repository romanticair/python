"""
在python中捕获信号；将信号编号N作为命令行参数传入，利用shell命令
"kill -N pid" 向这个进程发生信号；大多数信号处理器在捕获信号后转到python
中处理;signal模块在Windows下可以，不过仅定义了少数几种信号类型，且没os.kill；
"""
import sys
import signal
import time


def now():
    return time.ctime(time.time())            # 当前时间


def on_signal(signum, stackframe):           # python信号处理器
    print('Got signal', signum, 'at', now())   # 多数信号处理器一直有效

signum = int(sys.argv[1])
signal.signal(signum, on_signal)               # 布置信号处理器
while True:
    signal.pause()                             # 等待信号(或pass)