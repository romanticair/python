# !/usr/bin/python
# -*-coding:utf-8-*-

"""
split and interactively page a string, file, or stream of
text to stdout; when run as a script, page stdin or file
whose name is passed on cmdline; if input is stdin, can't
use it for user reply--use platform-specific tools or GUI;
"""

import sys


def getreply():
    """
    读取交互式用户的回复键，即使stdin重定向到某个文件或者管道
    """
    if sys.stdin.isatty():             # 如果stdin是控制台
        return input('?')             # 从stdin读取回复行数据
    else:
        if sys.platform[:3] == 'win':  # 如果stdin重定向
            import msvcrt             # 不能用于询问用户
            msvcrt.putch(b'?')
            key = msvcrt.getche()      # 使用windows控制台工具
            msvcrt.putch(b'\n')        # getch()方法不能回应键
            return key
        else:
            # linux?: open('/dev/tty').readline().[:-1]
            assert False, 'platform not supported'


def more(text, numlines=10):
    """
    page multiline string to stdout
    """
    lines = text.splitlines()
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk:
            print(line)
        if lines and getreply() not in [b'y', b'Y']:
            break

if __name__ == '__main__':
    if len(sys.argv) == 1:                  # 不存在命令行参数
        more(sys.stdin.read())              # 在stdin页没有输入数据
    else:
        more(open(sys.argv[1]).read(), 10)  # 其它文件名参数


