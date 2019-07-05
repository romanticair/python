import sys


def filter_files(name, function):    # 通过函数筛选文件
    input = open(name, 'r')
    output = open(name + '.out', 'w')   # 显示指定输出文件
    for line in input:
        output.write(function(line))    # 写入修改后的行
    input.close()
    output.close()


def filter_stream(function):
    while True:                        # 使用标准流
        line = sys.stdin.readline()     # 或者使用：input()
        if not line:
            break
        print(function(line), end='')    # 或者使用：sys.stdout.write()

if __name__ == '__main__':
    filter_stream(lambda line: line)    # 如果运行，则将stdin复制到stdout 