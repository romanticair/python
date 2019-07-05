"""执行API调用并处理结果，找出GitHub上新级最高的Python项目
使这些数据可视化出来"""
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# 执行API调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
# 返回json结果
r = requests.get(url)
print('Status code:', r.status_code)

# 将API响应存储在一个变量中
response_dicts = r.json()
print('Total repositories', response_dicts['total_count'])

# 搜索有关仓库的消息
repo_dicts = response_dicts['items']
print('Repositories retured:', len(repo_dicts))

##############################################################################
# 初步探究API
##############################################################################

# 研究第一个仓库
# repo_dict = repo_dicts[0]
# print('\nKeys: ', len(repo_dict))
# for key in sorted(repo_dict.keys()):
#     print(key)

# print('\nSelected information about first repository:')
# for repo_dict in repo_dicts:
#     print('\nName:', repo_dict['name'])
#     print('Owner:', repo_dict['owner']['login'])
#     print('Stars:', repo_dict['stargazers_count'])
#     print('Repository:', repo_dict['html_url'])
#     print('Description:', repo_dict['description'])

"""
# 研究星级排名
names, stars = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])

# 可视化
my_style = LS('#336699', base_style=LCS)
# x标签45°旋转，并隐藏了图例
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', stars)
chart.render_to_file('python_repos01.svg')
##############################################################################
# 改进图表样式，想调整代码结构
##############################################################################

# 可视化
my_style = LS('#336699', base_style=LCS)
# x标签45°旋转，并隐藏了图例
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24        # 图表标题
my_config.label_font_size = 14        # 副标题(xy轴大部分刻度数字)
my_config.major_label_font_size = 18  # 主标题(y轴上n个整数倍的刻度数值)
my_config.truncate_label = 15         # 缩短较长的项目名(15个char)
my_config.show_y_guides = False      # 隐藏图表中的水平线
my_config.width = 1000                # 图表自定义宽度

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', stars)
chart.render_to_file('python_repos01.svg')
"""

##############################################################################
# 根据数据绘图, 包含API调用返回的30个项目的消息
##############################################################################
"""

names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    star = repo_dict.get('stargazers_count', 'Nothing')
    description = repo_dict.get('description', 'Nothing')  # description 出现了NoneType
    plot_dict = {
        'value': star,
        'label': description,
    }
    plot_dicts.append(plot_dict)

# 可视化
my_style = LS('#336699', base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24        # 图表标题
my_config.label_font_size = 14        # 副标题(xy轴大部分刻度数字)
my_config.major_label_font_size = 18  # 主标题(y轴上n个整数倍的刻度数值)
my_config.truncate_label = 15         # 缩短较长的项目名(15个char)
my_config.show_y_guides = False      # 隐藏图表中的水平线
my_config.width = 1000                # 图表自定义宽度

print(plot_dicts)
chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', plot_dicts)
chart.render_to_file('python_repos02.svg')

"""

##############################################################################
# 在图表中添加可单击的链接(最终版本)
##############################################################################
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    plot_dict = {
        'value': repo_dict['stargazers_count'],
        # 'label': repo_dict['description'],
        'xlink': repo_dict['html_url'],           # 将每个条形都转换为活跃的链接
    }
    plot_dicts.append(plot_dict)

# 可视化
my_style = LS('#336699', base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24        # 图表标题
my_config.label_font_size = 14        # 副标题(xy轴大部分刻度数字)
my_config.major_label_font_size = 18  # 主标题(y轴上n个整数倍的刻度数值)
my_config.truncate_label = 15         # 缩短较长的项目名(15个char)
my_config.show_y_guides = False      # 隐藏图表中的水平线
my_config.width = 1000                # 图表自定义宽度

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', plot_dicts)
chart.render_to_file('python_repos03.svg')
