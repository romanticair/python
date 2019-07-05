"""派生出子线程，直到你输入'q'"""
import _thread


def child(tid):
    print('Hello from thread', tid)


def parent():
    i = 0
    while True:
        i += 1
        _thread.start_new_thread(child, (i,))  # 每条信息由新线程打印出来，随机退出
        if input() == 'q':
            break

parent()