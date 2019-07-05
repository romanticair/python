"""
file-like objects that save standard output text in a string and provide
standard input text from a string; redirect runs a passed-in function
with its output and input streams reset to these file-like class objects;
"""

import sys


class Output:                       # 模拟输出文件
    def __init__(self):
        self.text = ''                # 新建空字符串

    def write(self, string):         # 添加字节字符串
        self.text += string

    def writelines(self, lines):    # 在列表中添加每一行数据
        for line in lines:
            self.write(line)


class Input:                         # 模拟输入文件
    def __init__(self, input=''):     # 默认参数
        self.text = input

    def read(self, size=None):       # 可选参数
        if size is None:              # 读取 N 个字节，或者所有字节
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:size], self.text[size:]
        return res

    def readline(self):
        eoln = self.text.find('\n')     # 查找下一个eoln的偏移位置
        if eoln == -1:                  # 清晰 elon， 其值为-1
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:eoln+1], self.text[eoln+1:]
        return res


# test: (result, output) = redirect(interact, (), {}, '4\n5\n6\n')
def redirect(function, pargs, kargs, input):  # 重定向 stdin/out
    savestreams = sys.stdin, sys.stdout         # 运行函数对象
    sys.stdin = Input(input)                    # 返回stdout文件
    sys.stdout = Output()
    try:
        result = function(*pargs, **kargs)      # 运行带参数的函数
        output = sys.stdout.text
    finally:
        sys.stdin, sys.stdout = savestreams     # 如果存在exc或者其它，重新存储数据
    return result, output                      # 如果不存在exc,返回结果


