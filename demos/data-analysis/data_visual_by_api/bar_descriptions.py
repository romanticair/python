##############################################################################
# 添加自定义工具提示(光标位于图标上有信息提示)
###############################################################################

import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

my_style = LS('#333366', base_style=LCS)
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title = 'Python Projects'
chart.x_labels = ['httpie', 'django', 'flask']

# 使用label给条形图创建工具提示
plot_dicts = [
    {'value': 16101, 'label': 'Description of httpie.'},
    {'value': 15028, 'label': 'Description of django.'},
    {'value': 14798, 'label': 'Description of flask.'}
]
chart.add('', plot_dicts)
chart.render_to_file('bar_description.svg')
