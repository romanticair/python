"""
测试连接标准流到文本和二进制模式文件的效果，同样保持socket.makefile为True：输出需要
文本模式，但是文本模式会排除无缓冲模式 ---- 使用 -u或sys.stdout.flush()调用
"""
import sys


def reader(F):
    tmp, sys.stdin = sys.stdin, F
    line = input()
    print(line)
    sys.stdin = tmp

reader(open('test_stream_modes.py'))        # works: input() returns text
reader(open('test_stream_modes.py', 'rb'))  # works: but input() returns bytes


def writer(F):
    tmp, sys.stdout = sys.stdout, F
    print(99, 'spam')
    sys.stdout = tmp

writer(open('temp', 'w'))                   # works: print() passes text str to .write()
print(open('temp').read())

writer(open('temp', 'wb'))                  # FAILS on print: binary mode requires bytes
writer(open('temp', 'w', 0))                # FAILS on open: text must be unbuffered
