"""每次都打印200，因为共享资源访问已经同步化"""
import threading
import time

count = 0


def adder(addlock):       # 传入共享的锁对象
    global count
    with addlock:
        count += 1         # 围绕stmt自动获得/释放锁
    time.sleep(0.5)
    with addlock:
        count += 1         # 同一时间只有1个线程进行更新

alllock = threading.Lock()
threads = []
for i in range(100):
    thread = threading.Thread(target=adder, args=(alllock,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
print(count)