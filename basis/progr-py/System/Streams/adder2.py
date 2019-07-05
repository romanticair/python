import sys

sum = 0
while True:
    line = sys.stdin.readline()  # 包含了\n，不必用[:-1]或rstrip()移除它
    if not line:
        break
    sum += int(line)
print(sum)
