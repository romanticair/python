# 非图形用户界面端：将流连接到套接字并正常执行

import time
import sys

if len(sys.argv) > 1:                        # 仅当被请求时才链接到图形用户界面
    from socket_stream_redirect0 import *   # 将sys.stdout与套接字连接
    redirectOut()                             # 图形用户界面必须首先照常开启

# 非图形用户界面代码
while True:                                 # 将数据打印到标准输出
    print(time.asctime())                    # 通过套接字发送到图形用户界面进程
    sys.stdout.flush()                       # 发送前必须刷新：已缓存！
    time.sleep(2.0)                           # 无缓冲模式不可用，-u参数无法使用
