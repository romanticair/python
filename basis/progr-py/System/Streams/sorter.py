"""Dos: python sorter.py < data"""

import sys

lines = sys.stdin.readlines()  # 或者sorted(sys.stdin)排序方法
lines.sort()                   # 对输入的数据进行排序
for line in lines:
    print(line, end='')        # 发送结果到stdout
