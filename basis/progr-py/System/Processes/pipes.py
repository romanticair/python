"""
派生一个子进程/程序，连接我的stdin/stdout和子进程的stdin/stdout；
我的读写映射到派生程序的输出和输入上；很像利用subprocess模块绑定流一样。
"""
import os
import sys


def spawn(prog, *args):                        # 传入程序名称，命令行参数
    stdinFd = sys.stdin.fileno()                # 获得流的描述符
    stdoutFd = sys.stdout.fileno()              # 一般stdin=0, stdout=1

    parentStdin, childStdout = os.pipe()        # 创建两个IPC管道频道
    childStdin, parentStdout = os.pipe()        # pipe返回(输入流文件描述符，输出流文件描述符)
    pid = os.fork()                             # 创建一个此进程的副本
    if pid:
        os.close(childStdout)                   # 分支之后，在父进程中：
        os.close(childStdin)                    # 在父进程中关闭子进程端
        os.dup2(parentStdin, stdinFd)           # 我的sys.stdin副本复制为pipe1[0]
        os.dup2(parentStdout, stdoutFd)         # 我的sys.stdout副本复制为pipe2[1]
    else:
        os.close(parentStdin)                   # 分支之后，在子进程中：
        os.close(parentStdout)                  # 在子进程中关闭父进程端
        os.dup2(childStdin, stdinFd)            # 我的sys.stdin副本复制为pipe2[0]
        os.dup2(childStdout, stdoutFd)          # 我的sys.stdin副本复制为pipe1[1]
        args = (prog, args)
        os.execvp(prog, args)                   # 这个进程中的新程序
        assert False, 'execvp failed!'        # 不让os.exec调用返回到这里

if __name__ == '__main__':
    mypid = os.getpid()
    spawn('python', 'pipes_testchild.py')           # 分支子程序

    print('Hello 1 from parent', mypid)             # 发送到子进程的stdin
    sys.stdout.flush()                              # 清理stdio缓冲区
    reply = input()                                 # 发自子进程的stdout
    sys.stderr.write('Parent got: "%s"\n' % reply)  # stderr没有绑定在管道上

    print('Hello 2 from parent', mypid)
    sys.stdout.flush()
    reply = sys.stdin.readline()
    sys.stderr.write('Parent got: "%s"' % reply[:-1])
