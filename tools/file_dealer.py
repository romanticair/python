import os
import sys
import fnmatch


def rename(f_path, f_suffix, f_max=20):
    """
    批处理同一文件夹下的文件(顺序命名...)。改变工作路径,进入给定文件夹路径里，对给定扩展名的
    文件进行遍历处理，以数字顺序形式重新命名给定文件路径下指定文件拓展名的文件名。

    Args:
        f_path: 文件夹路径
        f_suffix: 文件后缀名
        f_max: 命名文件数量

    Returns: None
    
    """
    f_counts = 0
    f_cur = 1
    os.chdir(f_path)
    f_list = list(map(str.lower, os.listdir()))
    sort_by_filename(f_list)
    for f_name in f_list:
        if f_name.endswith(f_suffix):
            if f_counts > f_max:
                break
            if f_name.split('.')[0] == str(f_cur):
                f_cur += 1
                continue
            os.rename(f_name, str(f_cur) + f_suffix)
            f_counts += 1
            f_cur += 1

    if f_counts > 1:
        print(f_counts, ' files have been renamed.')
    else:
        print(f_counts, ' file have been renamed.')


def sort_by_filename(alist):
    """
    为排序文件而自定义的一个排序, 小的在前。

    Args:
        alist: 文件名列表

    Returns: None

    """
    for i in range(len(alist) - 1):
        s1 = alist[i].split('.')[0]
        if s1.isdigit():
            for j in range(i + 1, len(alist)):
                s2 = alist[j].split('.')[0]
                if s2.isdigit():
                    if int(s1) > int(s2):
                        alist[i], alist[j] = alist[j], alist[i]
                        s1 = alist[i].split('.')[0]
                else:
                    alist.append(alist[j])
                    del alist[j]
        else:
            alist.append(alist[i])
            del alist[i]


def find(pattern, startdir=os.curdir):
    """
    返回某个根目录及其子目录下所有匹配某个文件名模式的文件，使用 os.walk 循
    环，不支持修建子目录。本函数是一个生成器，利用 os.walk() 生成器产生匹配的文件名

    Args:
        pattern: 文件名模式
        startdir: 根目录

    yield: 匹配模式的文件绝对路径字符串

    """
    for (thisDir, subsHere, filesHere) in os.walk(startdir):
        # 遍历子目录列表和文件列表
        for name in subsHere + filesHere:
            if fnmatch.fnmatch(name, pattern):
                fullpath = os.path.join(thisDir, name)
                yield fullpath


def find_list(pattern, startfir=os.curdir, dosort=False):
    """
    利用 find() 生成器收集符合文件模式的文件名路径，以结果列表返回。

    Args:
        pattern: 文件名模式
        startfir: 根目录
        dosort: 排序标识符

    Returns: 结果列表

    """
    matches = list(find(pattern, startfir))
    if dosort:
        matches.sort()
    return matches


def search_key(startdir, searchkey):
    """
    搜索指定的目录及其子目录下所有含有指定的字符串的文件。首先利用 os.walk
    接口而不是 find 来收集文件名，类似于用 find 搜索 "*" 模式的每个
    返回结果然后调用 visit_file 搜索字符串来进行查找。

    Args:
        startdir: 根目录
        searchkey: 要搜索的字符串

    Returns: 结果列表

    """
    result = []
    for (thisDir, subsHere, filesHere) in os.walk(startdir):
        for fname in filesHere:
            fpath = os.path.join(thisDir, fname)
            contain = visit_file(fpath, searchkey)
            if contain:
                result.append(fpath)

    return result


def visit_file(fpath, searchkey):
    """
    对于每个非目录文件进行迭代，搜索字符串

    Args:
        fpath: 完整的文件路径
        searchkey: 要搜索的字符串

    Returns: boolean

    """
    # 在指定的文件类型里查找
    textexts = ['.py', '.pyw', '.txt', '.c', '.h']
    try:
        if os.path.splitext(fpath)[1] not in textexts:
            print('Skipping {0} ☆ -'.format(fpath))
        else:
            with open(fpath, 'r', encoding='utf-8') as contents:
                for content in contents.readlines():
                    if searchkey in content:
                        print('Found {0} ★ +'.format(fpath))
                        return True
    except:
        print('Failed:', fpath, sys.exc_info()[0])

    return False

