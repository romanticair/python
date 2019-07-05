import random


def conflict(status, nextY):
    nextX = len(status)              # the numbers of rows
    for i in range(nextX):          # 从第一行开始, 检查各行是否与前面成对角或同列关系
        if abs(status[i] - nextY) in (0, nextX - i):   # 同列满足0, 对角线满足nextX - i
            return True
    return False


def queens(num = 8, status = ()):
    for pos in range(num):  # 遍历所有可能的位置
        if not conflict(status, pos):  # 如果不冲突
            if len(status) == num - 1:   # total number of queens
                yield (pos,)       # 返回无冲突的位置
    # The queens except the last one
            else:
                for result in queens(num, status + (pos,)):   # 此处将所有可能进行递归
                    print((pos,), "+", result, "=", (pos,) + result)
                    yield (pos,) + result


def Print(solution):
    def line(pos, length = len(solution)):
        return ' | ' * (pos) + ' Q ' + ' | ' * (length - pos - 1)

    for pos in solution:
        print(line(pos))

if __name__ == '__main__':
    Print(random.choice(list(queens())))

"""
from itertools import permutations

for vec in permutations(range(8)):
    if (8 == len(set(vec[i] + i for i in range(8))) == len(set(vec[i] - i for i in range(8)))):
        print(vec)
"""
