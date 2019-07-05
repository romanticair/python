"""用pygal可视化随机漫步的路径"""
import pygal
from random_walk import RandomWalk

# 创建一个随机漫步实例
rw = RandomWalk(num_points=10000)
# 实例开始漫步
rw.fill_walk()
# 获取漫步的x,y路径列表
x = rw.x_values
y = rw.y_values

# 研究一下可以用什么图??????
# 可视化数据
xy_chart = pygal.XY(stroke=False)
xy_chart.title = '随机漫步10000步'
xy_chart.x_title = '左右'
xy_chart.y_title = '上下'
xy_chart.add('A6', list(zip(x, y)))     # 标注线
xy_chart.render_to_file('random_visual.svg')
