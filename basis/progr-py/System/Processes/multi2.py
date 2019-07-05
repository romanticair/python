"""
使用多进程匿名管道进行通信，返回两个connection对象来分别代表管道的两端；
对象从一端发送，在另一端接受，不过管道默认是双向的；
"""
import os
from multiprocessing import Process, Pipe


def sender(pipe):
    """在匿名管道上向父进程发送对象"""
    pipe.send(['spam'] + [42, 'eggs'])
    pipe.close()


def talker(pipe):
    """通过管道发送和接受对象"""
    pipe.send(dict(name='bob', spam=42))
    reply = pipe.recv()
    print('takler got:', reply)


if __name__ == '__main__':
    parentEnd, childEnd = Pipe()
    Process(target=sender, args=(childEnd,)).start()          # 派生带有管道的子进程
    print('parent got:', parentEnd.recv())                    # 从子进程处接收
    parentEnd.close()                                         # 或者在全局目录中自动关闭

    parentEnd, childEnd = Pipe()
    child = Process(target=talker, args=(childEnd,)).start()
    print('parent got:', parentEnd.recv())                    # 从子进程处接收
    parentEnd.send({x * 2 for x in 'spam'})                  # 向子进程发送
    parentEnd.close()                                         # 等待子进程退出
    print('parent exit.')
