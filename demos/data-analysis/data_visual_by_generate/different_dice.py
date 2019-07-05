"""使用pygal可视化投掷不同骰子的结果"""

import pygal
from die import Die

# 创建一个D6和一个D10
die_1 = Die()
die_2 = Die(10)
# 抛骰子多次，并将结果存储在一个列表中
results = []
for roll_num in range(50000):
    result = die_1.roll() + die_2.roll()  # 计算每次的总点数
    results.append(result)

# 分析结果
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
for value in range(2, max_result):
    frequency = results.count(value)
    frequencies.append(frequency)

# 可视化结果
hist = pygal.Bar()
hist.title = 'Results of rolling D6 and D10 50000 times.'
hist.x_labels = [str(x) for x in range(2, max_result + 1)]
hist._x_title = 'Result'
hist._y_title = ' Frequency of Result'
hist.add('D6 + D10', frequencies)
hist.render_to_file('dice_diff_visual.svg')
