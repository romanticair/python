"""
#######################################################################
测试某一目录下的Python脚本，传入命令行参数，将stdin和管道连接，通过
捕获stdout、stderr和退出状态来探测运行失败，以及获得前一次运行输出的
回归记录。利用subprocess模块派生和控制流(类似Python 2.X中的os.popen3)，
并可跨平台运行，流在subprocess中均为二进制字节。测试用的测试、参数、输
出和错误均映射到子目录中的文件。

这是一个命令行脚本，使用可选的命令行参数作为测试目录名和强制生成标
识符。我们可以将它封装成一个可调用的函数，不过它的结果是消息和输出
文件，而在这种情况下似乎调用/返回模型用处不大。

建议的功能加强：可以扩展成通过测试脚本接受多组命令行参数和/或输入，
以多次运行同一个脚本(利用glob处理多个带有".in"后缀的输入文件名？)；
还可以将所有测试文件以不同扩展名保存在同一目录下以简化软件结构，不过
不过我个人倾向于在输出中以回归的方式记录预期/实际输出。
#######################################################################
"""

import sys
import os
import glob
import time
from subprocess import Popen, PIPE


# 配置参数
testdir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
forcegen = len(sys.argv) > 2
print('Start tester:', time.asctime())
print('in', os.path.abspath(testdir))


def verbose(*args):
    print('-' * 80)
    for arg in args:
        print(arg)


def quiet(*args):
    pass


trace = quiet

# 对待测的脚本运行glob
testpatt = os.path.join(testdir, 'Scripts', '*py')
testfiles = glob.glob(testpatt)
testfiles.sort()
trace(os.getcwd(), *testfiles)

numfail = 0
for testpath in testfiles:                  # 运行目录下的所有测试
    testname = os.path.basename(testpath)    # 去除目录路径

    # 获取输入和参数
    infile = testname.replace('.py', '.in')
    inpath = os.path.join(testdir, 'Inputs', infile)
    indata = open(inpath, 'rb').read() if os.path.exists(inpath) else b''

    argfile = testname.replace('.py', '.args')
    argpath = os.path.join(testdir, 'Args', argfile)
    argdata = open(argpath, 'rb').read() if os.path.exists(argfile) else ''

    # 定位输出和错误，清楚前次结果
    outfile = testname.replace('.py', '.out')
    outpath = os.path.join(testdir, 'Outputs', outfile)
    outpathbad = outpath + '.bad'
    if os.path.exists(outpathbad):
        os.remove(outpathbad)

    errfile = testname.replace('.py', '.err')
    errpath = os.path.join(testdir, 'Errors', errfile)
    if os.path.exists(errpath):
        os.remove(errpath)

    # 测试运行时使用重定向过的流
    pypath = sys.executable
    command = '%s %s %s' % (pypath, testpath, argdata)
    trace(command, indata)

    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.stdin.write(indata)
    process.stdin.close()
    outdata = process.stdout.read()
    errdata = process.stderr.read()          # 数据为字节
    exitstatus = process.wait()              # 要求二进制文件
    trace(outdata, errdata, exitstatus)

    # 分析结果
    if exitstatus != 0:
        print('ERROR status:', testname, exitstatus)  # 退出状态
    if errdata:
        print('ERROR stream:', testname, errpath)     # 保存错误文件
    if exitstatus or errdata:                        # 考虑两个都失败了的情况
        numfail += 1                                  # 可以获取退出状态及stderr
        open(outpathbad, 'wb').write(outdata)         # 方便以后查看保存输出
    elif not os.path.exists(outpath) or forcegen:
        print('generating:', outpath)                 # 没有输出目录就创建目录
        open(outpath, 'wb').write(outdata)
    else:
        priorout = open(outpath, 'rb').read()         # 或者与前次输出相比
        if priorout == outdata:
            print('passed:', testname)
        else:
            numfail += 1
            print('FAILED output:', testname, outpathbad)
            open(outpathbad, 'wb').write(outpath)

print('Finished:', time.asctime())
print('%s tests were run, %s tests failed.' % (len(testfiles), numfail))

















