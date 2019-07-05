"""使用matplotlib可视化投掷两个骰子的结果"""

import matplotlib.pyplot as plot
from die import Die

# 创建两个D6
die_1 = Die()
die_2 = Die()

# 投掷骰子，并将结果存储在一个列表中
results = []
for number_die in range(1000):
    result = die_1.roll() + die_2.roll()  # 得到的点数相加
    results.append(result)

# 分析结果(出现的次数)
analysis = []
for die_id in range(2, die_1.num_sides * 2 + 1):
    analysis.append(results.count(die_id))

# 数据可视化
plot.figure(figsize=(6, 10), dpi=128)    # 可视窗口大小 + 分辨率
plot.ylabel('The numbers of points')
plot.xlabel('D6 point')
plot.title('The results of two D6 die')
plot.plot(list(range(2, die_1.num_sides * 2 + 1)), analysis)
plot.show()
