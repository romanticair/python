"""
#####################################################################
用法："python diffall.py dir1 dir2"
递归的目录树比较：报告仅在dir1而非dir2中存在的特有文件，报告dir1和dir2
同名但内容不同的文件，报告在dir1和dir2中同名但不同类型的情况，并对dir1
和dir2下所有同名子目录及其目录进行相同操作。输出的末尾打印差异的终结，
不过其中的细节请在重定向的输出中搜索"DIFF"和"unique"字符串。

这个版本里传入结果以避免在dirdiff.comparedirs()中再次调用os.listdir()。
#####################################################################
"""
import os
import dirdiff

blocksize = 1024 * 1024        # 每次至多读取1MB


def intersect(seq1, seq2):
    """
    返回seq1和seq2的共有项；
    也可以使用set(seq1) & set(seq2)，不过集合内顺序是随机的，故而可能
    丢失任何依赖于平台的目录顺序。
    """
    return [item for item in seq1 if item in seq2]


def comparetrees(dir1, dir2, diffs, verbose=False):
    """
    比较两个目录数中的所有子目录和文件；使用二进制文件来阻止Unicode解码
    和换行符转换，因为目录树可能含有二进制文件和文本文件；可能需要listdir
    的bytes参数来处理某些平台上不可解码的文件名。
    """
    # 比较文件名列表
    print('-' * 80)
    names1 = os.listdir(dir1)
    names2 = os.listdir(dir2)
    if not dirdiff.comparedirs(dir1, dir2, names1, names2):
        diffs.append('unique files at %s - %s' % (dir1, dir2))

    print('Comparing contents')
    common = intersect(names1, names2)
    missed = common[:]

    # 比较共有的内容
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            file1 = open('path1', 'rb')
            file2 = open('path2', 'rb')
            while True:
                bytes1 = file1.read(blocksize)
                bytes2 = file2.read(blocksize)
                if (not bytes1) and (not bytes2):
                    if verbose:
                        print(name, 'matches')
                    break
                if bytes1 != bytes2:
                    diffs.append('files differ at %s - %s' % (path1, path2))
                    print(name, 'DIFFERS')
                    break

    # 递归比较共有目录
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparetrees(path1, path2, diffs, verbose)

    for name in missed:
        diffs.append('files missed at %s - %s: %s' % (dir1, dir2, name))
        print(name, 'DIFFERS')

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    diffs = []
    comparetrees(dir1, dir2, diffs, True)                   # 原位修改差异
    print('=' * 40)                                          # 遍历，报告差异列表
    if not diffs:
        print('No diffs found.')
    else:
        print('Diffs found:', len(diffs))
        for diff in diffs:
            print('-', diff)