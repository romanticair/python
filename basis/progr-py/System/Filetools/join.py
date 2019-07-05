#!usr/bin/python

"""
合并split.py创建的目录下的所有组分文件以重建文件。
大概相当于Unix下的"cat fromdir/* > tofile"命令，不过可移植性和可配置
性更好，并且将合并操作作为可以重复使用的函数而输出。依赖文件名的排序顺
序：长度必须一致。可以进一步扩展分割/合并，弹出Tkinter文件选择器。
"""
import os
import sys

readsize = 1024


def join(fromdir, tofile):
    output = open(tofile, 'wb')
    parts = os.listdir(fromdir)
    parts.sort()
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj = open(filepath, 'rb')
        while True:
            filebyts = fileobj.read(readsize)
            if not filebyts:
                break
            output.write(filebyts)
        fileobj.close()


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: join.py [from-fir-name to-file-name]')
    else:
        if len(sys.argv) != 3:
            interactive = True
            fromdir = input('Directory containing part files?')
            tofile = input('Name of file to be recreated?')
        else:
            interactive = False
            fromdir, tofile = sys.argv[1:3]
        absfrom, absto = map(os.path.abspath, [fromdir, tofile])
        print('Joining ', absfrom, ' to make ', absto)

        try:
            join(absfrom, absto)
        except Exception:
            print('Error joning files:')
            print(sys.exc_info()[0], sys.exc_info()[1])
        else:
            print('Join complete: see ', absto)
        if interactive:
            input('Press Enter Key')  # 如果单击运行脚本则再次暂停
