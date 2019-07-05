"""
分割字符串或文本文件并交互地进行分页
"""


def more(text, numlines=15):
    lines = text.splitlines()               # 效果类似split('\n'), 不过不用在末尾加''
    while lines:
        chunk = lines[:numlines]
        lines = lines[numlines:]
        for line in chunk:
            print(line)
        if lines and input('More?') not in ['Y', 'y']:
            break

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        more(sys.stdin.read())              # 不存在命令行参数
    else:
        more(open(sys.argv[1]).read(), 10)  # 显示命令行里的文件的页面内容
