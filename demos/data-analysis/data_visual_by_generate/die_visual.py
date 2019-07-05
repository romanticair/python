"""使用pygal可视化投掷单个骰子的结果"""
import pygal
from die import Die

# 创建一个D6
die = Die()
# 骰几次骰子，并将结果存储在一个列表中
results = []
for roll_num in range(1000):
    result = die.roll()
    results.append(result)

# 分析结果
frequencies = []
for value in range(1, die.num_sides + 1):
    frequency = results.count(value)
    frequencies.append(frequency)

# 对结果进行可视化
hist = pygal.Bar()
hist.title = 'Results of rolling one D6 1000 times.'
hist.x_labels = [str(x) for x in range(1, die.num_sides + 1)]
hist.x_title = 'Result'
hist.y_title = 'Frequency of Result'
hist.add('D6', frequencies)            # 将一系列值添加到图表中(D6代表值标签)
hist.render_to_file('die_visual.svg')  # 将图渲染成一个SVG文件
