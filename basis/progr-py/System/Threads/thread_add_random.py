"""windows 7下每次运行打印不同的结果"""

import threading
import time

count = 0


def adder():
    global count
    count += 1       # 更新全局作用域中一个共享的名称
    time.sleep(0.5)
    count += 1       # 线程共享对象内存及全局名称

threads = []
for i in range(100):
    thread = threading.Thread(target=adder, args=())
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(count)