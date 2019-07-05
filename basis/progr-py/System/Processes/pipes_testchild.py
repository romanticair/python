import os
import time
import sys

mypid = os.getpid()
parentpid = os.getppid()
sys.stderr.write('Child %d of %d got arg: "%s"\n' % (mypid, parentpid, sys.argv[1]))

for i in range(2):
    time.sleep(3)                                 # 通过这里的休眠让父进程等待
    recv = input()                                # stdin绑定到管道上：来自父进程的stdout
    time.sleep(3)
    send = 'Child %d got: [%s]' % (mypid, recv)
    print(send)                                   # stdout绑定到管道上：发至父进程的stdin
    sys.stdout.flush()                            # 去到数据已经发生，否则阻塞进程