"""
####################################################################################
针对GUI的系统范围的线程界面实用工具。

本程序实现了一个线程回调队列和由程序中所有窗口共享的检查器计时器循环；各工作线程对
要在主线程中执行的退出、运行操作进行排队；这样做不会阻塞GUI，而只是生成操作并管理、
调度退出和运行操作；工作线程既可与主线程自由重叠，也可与其它工作线程自由重叠。

针对可能出现多种线程同时运行（每一种线程都可能出现不同的退出操作）的情况，使用一个
回调函数和参数的队列比使用一个简单的数据队列更加有用。
由于GUI的API对于线程来说并不绝对安全，不才去按照线程的主要操作直接调用GUI更新回调
循坏中运行；这也使得GUI更新时的店不那么随机和不可预知；要将线程分成主操作、退出操作
和运行操作。

假设线程化的操作失败时引发异常，并具有 "process" 回调参数（如果该线程支持进度更新）；
再假设回调函数生命期短或者运行时由更新，并且队列包含用于图形用户界面应用程序中的回调
函数（或者其它可调用函数）----这需要一个小组件以便调度和捕捉 "after" 事件循环回调函数；
要在非图形用户下使用该模型，可改用简单的线程计时器；
####################################################################################
"""

# 即便标准库中没有线程也运行
try:                                      # 引发ImportError
    import _thread as thread             # 如果线程不可用
except ImportError:                      # 阻塞图形用户界面
    import _dummy_thread as thread       # 没有线程，但接口相同

# 共享的跨进程队列
# 在共享的全局作用域中命名，存活于共享的对象内存中
import queue
import sys

threadQueue = queue.Queue(maxsize=0)      # 大小不限

#############################################################################################
# 在主线程中----周期性地检查线程完成队列；在本主图形用户界面线程的队列中执行潜在的图形
# 用户界面动作；一个消费者（GUI），多个生产者（load、del和send）；同样可以使用一个简单
# 的列表：list.append和弹出原子；
# 每个计时器事件中最多执行N个动作：在每个计时器事件中对所有队列的回调进行循环可能会无期限
# 地阻塞图像用户界面，而仅仅执行一次回调可能会很耗时，或者因计时事件（如progress）而消耗
# CPU；假定回调生命周期短，或者在其运行时更新显示：执行完一次回调后，此处的代码重新调度，
# 返回事件循环并进行更新；由于这一无休止的循环在主线程中运行，不会阻止程序的退出。
#############################################################################################


def threadChecker(widget, delayMsecs=100, perEvent=1):           # 10次/秒，1个事件/计时器周期
    for i in range(perEvent):                                      # 设置传递速度
        try:
            (callback, args) = threadQueue.get(block=False)        # 运行至多N个回调
        except queue.Empty:
            break
        else:
            callback(*args)                                         # 此处运行回调
    widget.after(delayMsecs, lambda: threadChecker(widget, delayMsecs, perEvent))

################################################################################################
# 在新的线程中----运行动作，管理线程用于退出和执行的队列；想运行带有args的动作，然后运行带有
# 上下文的 on* 调用；这里加入队列的调用仅在主线程中调度，以避免并行的图形用户界面更新；这里
# 可以完全不用关注动作在线程中的使用；避免在线程中直接运行回调：线程中可能更新图形用户界面，因为
# 传递过来的、位于共享内存中的函数在线程中调用；progress回调仅向接受了传递过来的参数的队列中添加
# 回调；这里不更新运行时计数器：直到退出动作由threadChecker从队列中移除并在主线程中调度就才完成。
################################################################################################


def threaded(action, args, context, onExit, onFail, onProgress):
    try:
        if not onProgress:            # 等待该线程中的动作
            action(*args)              # 假定失败时引发异常
        else:
            def progress(*any):
                threadQueue.put((onProgress, any + context))
            action(progress=progress, *args)
    except:
        threadQueue.put((onFail, (sys.exc_info(),) + context))
    else:
        threadQueue.put((onExit, context))


def startThread(action, args, context, onExit, onFail, onProgress=None):
    thread.start_new_thread(threaded, (action, args, context, onExit, onFail, onProgress))

################################################################################################
# 线程安全的计数器或者标志位：当线程
# 更新其他不适由线程回调队列管理的共享状态时，可避免操作重叠。
################################################################################################


class ThreadCounter:
    def __init__(self):
        self.count = 0
        self.mutex = thread.allocate_lock()      # 也可使用Threading.semaphore

    def incr(self):
        self.mutex.acquire()                     # 也可使用self.mutex
        self.count += 1
        self.mutex.release()

    def decr(self):
        self.mutex.acquire()
        self.count -= 1
        self.mutex.release()

    def __len__(self):
        return self.count                      # 如果用作标志位，结果为True/False

################################################################################################
# 自测代码：将线程动作拆分为main、exit和progress
################################################################################################

if __name__ == '__main__':
    import time
    from tkinter.scrolledtext import ScrolledText

    def onEvent(i):                             # 生成线程的代码
        myname = 'thread-%s' % i
        startThread(action=threadaction,
                    args=(i, 3),
                    context=(myname,),
                    onExit=threadexit,
                    onFail=threadfail,
                    onProgress=threadprogress)

    # 线程的主要动作
    def threadaction(id, reps, progress):      # 线程的功能
        for i in range(reps):
            time.sleep(1)
            if progress:
                progress(i)                      # 回调，加入队列
        if id % 2 == 1:                          # 奇数表示失败
            raise Exception

    # 线程exit/progress回调：离开主线程队列
    def threadexit(myname):
        text.insert('end', '%s\text\n' % myname)
        text.see('end')

    def threadfail(exc_info, myname):
        text.insert('end', '%s\tfail\t%s\n' % (myname, exc_info[0]))
        text.see('end')

    def threadprogress(count, myname):
        text.insert('end', '%s\tprogress\t%s\n' % (myname, count))
        text.see('end')
        text.update()                            # 在这里生效，在主线程中运行

    # 创建封闭的图形用户界面，在主线程中启动计时器循环
    # 当鼠标单击时，批量产生工作线程，可能重叠

    text = ScrolledText()
    text.pack()
    threadChecker(text)                         # 在主线程中开启线程循环
    text.bind('<Button-1>', lambda event: list(map(onEvent, range(6))))
    text.mainloop()
