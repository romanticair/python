# 非图形用户界面端：正常进行，不需要特别的代码

import time

while True:
    print(time.asctime())    # 发送给图形用户界面进程
    time.sleep(2.0)          # 此处不需要刷新
