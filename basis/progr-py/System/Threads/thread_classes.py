"""
带有状态和run()行为的线程类实例；使用较高层面上的类Java的
threading模块对象连接方法(而非mutexes或共享全局变量)在主线
程中探知线程结束时间；关于threading模块的更多细节请参考库手册
"""
import threading


class MyThread(threading.Thread):                     # 子类化
    def __init__(self, myid, count, mutex):
        threading.Thread.__init__(self)
        self.myid = myid
        self.count = count
        self.mutex = mutex                              # 共享对象，不是全局对象

    def run(self):                                     # run函数提供线程逻辑业务
        for i in range(self.count):                    # 仍然同步化stdout访问
            with self.mutex:
                print('[%s] => %s' % (self.myid, i))

stdoutmetex = threading.Lock()                          # 与thread.allocate_lock()相同
threads = []
for i in range(5):                                     # 创建并开始5个线程
    thread = MyThread(i, 100, stdoutmetex)
    thread.start()                                      # 线程中开始运行run方法
    threads.append(thread)

for thread in threads:
    thread.join()                                     # 等待线程退出
print('Main thread exiting.')