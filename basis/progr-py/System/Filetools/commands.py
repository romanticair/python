#!/usr/local/bin/python

from sys import argv
from scanfile import scanner


class UnknownCommand(Exception):pass


def process_line(line):
    if line[0] == '*':            # 应用到每一行
        print('Ms.', line[1:-1])  # 剥去开头和末尾字符：\n
    elif line[0] == '+':
        print('Mr.', line[1:-1])
    else:
        raise UnknownCommand(line)

filename = 'data.txt'
if len(argv) == 2:
    filename = argv[1]            # 允许通过文件名命令行参数传入文件
scanner(filename, process_line)   # 运行扫描器
