"""国家人口数据统计可视化"""
import json
from pygal.maps.world import World
from countries import get_country_code


# 将数据加载到一个列表中
filename = 'population_data.json'
with open(filename) as f:
    pop_data = json.load(f)

# 只打印每个国家2010年的人口数量
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        # population = int(pop_dict['Value'])       # 包含浮点数的字符串转换不了为整数
        population = int(float(pop_dict['Value']))  # 以防万一(转浮点后再转整)
        code = get_country_code(country_name)       # 获取国别码
        if code:
            print(country_name + ': ' + str(population))
        else:
            print('ERROR - ' + country_name)

"""
# 创建一个包含人口数量的字典
cc_populations = {}
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_populations[code] = population

wm = World()
wm.title = 'World Population in 2010, by Country'
wm.add('2010', cc_populations)  # 让其自动映射
wm.render_to_file('world_population01.svg')

################################################################
# 由于有些国家数据缺失(国家呈黑色)，还有人口数量划分问题，颜色的
# 深浅不足以反映国家人口的差别，现根据对人口数量对国家分组
################################################################

cc_populations = {}
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_populations[code] = population

# 根据人口数量将所有的国家分成三组
cc_pops_1, cc_pops_2, cc_pops_3 = {}, {}, {}
for cc, pop in cc_populations.items():
    if pop < 10000000:           # 少于1000万的
        cc_pops_1[cc] = pop
    elif pop < 1000000000:       # 介于1000万和10亿间的
        cc_pops_2[cc] = pop
    else:                        # 10亿以上的
        cc_pops_3[cc] = pop

wm = World()
wm.title = 'World Population in 2010, by Country'
wm.add('0-10m', cc_pops_1)        # 三种不同的颜色
wm.add('10m-1bn', cc_pops_2)      # 可明显地看到人口数量上的差别
wm.add('>1bn', cc_pops_3)
wm.render_to_file('world_population02.svg')
"""

################################################################
# 按人口将国家分组很有效，但默认颜色太随机了，我们选择更鲜艳的粉
# 色和绿色基色，让我们设置样式调整颜色，指定一种基色。
################################################################
"""

from pygal.style import RotateStyle

cc_populations = {}
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_populations[code] = population

# 根据人口数量将所有的国家分成三组
cc_pops_1, cc_pops_2, cc_pops_3 = {}, {}, {}
for cc, pop in cc_populations.items():
    if pop < 10000000:           # 少于1000万的
        cc_pops_1[cc] = pop
    elif pop < 1000000000:       # 介于1000万和10亿间的
        cc_pops_2[cc] = pop
    else:                        # 10亿以上的
        cc_pops_3[cc] = pop

# 该类需提供一个十六进制的RGB(红绿蓝)颜色的实参(根据这个颜色进行分组)
wm_style = RotateStyle('#336699')
wm = World(style=wm_style)
wm.title = 'World Population in 2010, by Country'
wm.add('0-10m', cc_pops_1)        # 三种不同的颜色
wm.add('10m-1bn', cc_pops_2)      # 可明显地看到人口数量上的差别
wm.add('>1bn', cc_pops_3)
wm.render_to_file('world_population03.svg')

################################################################
# 加亮颜色主题
################################################################
from pygal.style import LightColorizedStyle

# 该类修改整个图表的主题，包括背景色、标签国家颜色
wm_style = LightColorizedStyle
# 再使用RotateStyle创建一个样式，并传入另一个实参base_style
wm_style = RotateStyle('#336699', base_style=LightColorizedStyle)
"""

