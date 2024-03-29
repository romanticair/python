# 将文本文件打包成一个文件，文件之间用行隔开

import sys
import glob

marker = ':' * 20 + 'textpak=>'                          # 让用于分割的行是独特的


def pack(ofile, ifiles):
    output = open(ofile, 'w')
    for name in ifiles:
        print('packing:', name)
        finput = open(name, 'r').read()                  # 打开下一个输入的文件
        if finput[-1] != '\n':                           # 确保该文件末行是分割行
            finput += '\n'
        output.write(marker + name + '\n')               # 写入分割行
        output.write(finput)                             # 写入文件内容

if __name__ == '__main__':
    ifiles = []
    for patt in sys.argv[2:]:
        ifiles += glob.glob(patt)                        # Windows 下不会自动glob
    pack(sys.argv[1], ifiles)                            # 将命令行中列出的文件打包


