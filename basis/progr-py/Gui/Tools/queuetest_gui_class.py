# 显示工作线程所生成和加入队列的数据的图形界面（基于类）

import threading
import queue
import time
from tkinter.scrolledtext import ScrolledText


class ThreadGui(ScrolledText):
    threadsPerClick = 4

    def __init__(self, parent=None):
        ScrolledText.__init__(self, parent)
        self.pack()
        self.dataQueue = queue.Queue()
        self.bind('<Button-1>', self.makeThreads)
        self.consumer()

    def consumer(self):
        try:
            print('get')
            data = self.dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            self.insert('end', 'consumer got => %s\n' % str(data))
            self.see('end')
        self.after(250, self.consumer)

    def producer(self, id):
        for i in range(5):
            time.sleep(0.1)
            print('put')
            self.dataQueue.put('[producer id=%d, count=%d]' % (id, i))

    def makeThreads(self, event):
        for i in range(self.threadsPerClick):
            threading.Thread(target=self.producer, args=(i,)).start()

if __name__ == '__main__':
    root = ThreadGui()
    root.mainloop()
