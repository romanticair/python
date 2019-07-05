# 显示工作线程生成和加入队列的数据的图形界面

import _thread
import queue
import time

dataQueue = queue.Queue()  # 不限大小


def producer(id):
    for i in range(5):
        time.sleep(0.1)
        print('put')
        dataQueue.put('[producer id=%d, count=%d]' % (id, i))


def consumer(root):
    try:
        print('get')
        data = dataQueue.get(block=False)
    except queue.Empty:
        pass
    else:
        root.insert('end', 'consumer got => %s\n' % str(data))
        root.see('end')
    root.after(250, lambda: consumer(root))        # 每秒4次


def makethreads():
    for i in range(4):
        _thread.start_new_thread(producer, (i,))

if __name__ == '__main__':
    # gui主线程，当每次鼠标单击时，批量生产辅助线程
    from tkinter.scrolledtext import ScrolledText
    root = ScrolledText()
    root.pack()
    root.bind('<Button-1>', lambda event: makethreads())
    consumer(root)       # 在主线程中开始队列检查循环
    root.mainloop()      # 弹出式窗口，进入tk事件循环
