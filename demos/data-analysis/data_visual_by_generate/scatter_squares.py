"""绘制散点图"""

import matplotlib.pyplot as plt

x_values = list(range(1, 1001))
y_values = [x**2 for x in x_values]
# 点的颜色默认为蓝色点和黑色轮廓，而后者可能影响视觉效果
# plt.scatter(x_values, y_values, c='red', edgecolors='none', s=40)   # 删除数据点轮廓并改变颜色
# 或者三元组,越接近0颜色越深, 越接近1越浅
# plt.scatter(x_values, y_values, c=(0, 0, 0.8), edgecolors='none', s=40)
# 或者使用内置颜色映射, 使数据点的颜色由浅至深
plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=40)  # s代表点的粗细
# 设置图表标题并给坐标轴加上指定标签
plt.title('Square Numbers', fontsize=24)
plt.xlabel('Value', fontsize=14)
plt.ylabel('Square of Value', fontsize=14)

# 设置刻度标记的大小
plt.tick_params(axis='both', which='major', labelsize=14)
# 设置每个坐标轴的取值范围x(0, 1100), y(0, 1100000)
plt.axis([0, 1100, 0, 1100000])
# 将图表保存到文件(第二个参数指定将图表多余的空白区域裁减掉)
# plt.savefig('squares_plot.png', bbox_inches='tight')
plt.show()
