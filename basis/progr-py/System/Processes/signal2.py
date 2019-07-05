"""
在python中设置和捕获定时暂停信号，time.sleep和定时合用效果可能不好，
在这里使用signal.pause来暂停操作，直到接收到信号；
"""
import sys
import signal
import time


def now():
    return time.asctime()


def on_signal(signum, stackframe):           # python信号处理器
    print('Got signal', signum, 'at', now())   # 多数信号处理器一直有效

while True:
    print('Setting at', now())
    signal.signal(signal.SIGALRM, on_signal)
    signal.alarm(5)
    signal.pause()
    