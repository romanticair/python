"""将随机漫步的所有点绘制出来"""

import matplotlib.pyplot as plt
from random_walk import RandomWalk

# 只要程序处于活动状态，就不断地模拟随机漫步
while True:
    # 创建一个RandomWalk实例，并将其包含的点都绘制出来
    rw = RandomWalk(50000)
    rw.fill_walk()
    point_numbers = list(range(rw.num_points))
    # 设置绘图窗口的尺寸, 用于指定图标的(宽度,高度)英寸、分辨率(dpi)、背景色
    plt.figure(figsize=(10, 6))
    # 绘制每个漫步点的颜色, 把各点的向后顺序可视化出来
    plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Blues, s=1)
    # 突出起点和终点
    plt.scatter(0, 0, c='green', edgecolors='none', s=100)
    plt.scatter(rw.x_values[-1], rw.y_values[-1], c='red', edgecolors='none', s=100)
    # 隐藏坐标轴
    # plt.axes().get_xaxis().set_visible(False)
    # plt.axes().get_yaxis().set_visible(False)
    plt.show()
    keep_running = input("Make another walk? (y/n): ")
    if keep_running == 'n':
        break

# 只要程序处于活动状态，就不断地模拟花粉在水滴的运动路径
while True:
    rw = RandomWalk(5000)
    rw.fill_walk()
    plt.figure(figsize=(10, 6))
    plt.plot(rw.x_values, rw.y_values, linewidth=2)
    plt.show()
    keep_running = input("Make another walk? (y/n): ")
    if keep_running == 'n':
        break


