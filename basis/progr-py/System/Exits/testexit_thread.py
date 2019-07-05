"""
派生线程来观察共享全局内存的变化；线程通常在其运行的函数返回时退出；
但可以调用_thread.exit()结束其调用线程；_thread.exit和sys.exit相同，
也会抛出SystemExit异常；线程与可能被锁定的全局变量进行通信；小心：
在某些平台上可能需要做单元式的打印/输入调用-------stdout是共享的
"""
import _thread as thread

exitstat = 0


def child():
    global exitstat                               # 进程中的全局名称
    exitstat += 1                                  # 所有线程所共享
    threadid = thread.get_ident()
    print('Hello from child', threadid, exitstat)
    thread.exit()
    print('Never reached')


def parent():
    while True:
        thread.start_new_thread(child, ())
        if input() == 'q':
            break

if __name__ == '__main__':
    parent()