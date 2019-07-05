"""
还有很多工具：进程池、管理器、锁、条件等
"""
import os
from multiprocessing import Pool


def powers(x):
    # print(os.getpid())           # 能够监视子进程
    return 2 ** x

if __name__ == '__main__':
    works = Pool(processes=5)
    results = works.map(powers, [2]*100)
    print(results[:16])
    print(results[-2:])

    results = works.map(powers, range(100))
    print(results[:16])
    print(results[-2:])