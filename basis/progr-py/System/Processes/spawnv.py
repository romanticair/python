"""
启动10个并行运行的child.py副本；在Windows下用spawnv启动程序(类似fork/exec组合);
使用P_OVERLAY则进行替换，使用P_DETACH则子进程stdout不指向任何地方；现在也可以
使用可移植的subprocess或multiprocessing模块来完成！
"""
import os
import sys

for i in range(10):
    if sys.platform[:3] == 'win':
        pypath = sys.executable
        os.spawnv(os.P_NOWAIT, pypath, ('python', 'child.py', str(i)))
    else:
        pid = os.fork()
        if pid != 0:
            print('Process %d spawned' % pid)
        else:
            os.execlp('python', 'python', 'child.py', str(i))

print('Main process exiting.')