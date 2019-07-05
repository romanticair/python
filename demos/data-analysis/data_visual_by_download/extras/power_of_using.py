"""可视化1014年全国各国家电力使用量

数据来自 https://data.worldbank.org/indicator/ """

import csv


filename = 'API_EG.USE.ELEC.KH.PC_DS2_en_csv_v2_9987224.csv'
with open(filename, encoding='utf-8') as f:
    reader = csv.reader(f)
    title = next(reader)[1]     # 获取标题
    for i in range(4):
        next(reader)            # 跳过空行和题头

    # 收集各个国家的名称及其 1014(index=-5) 年的电力使用总量
    country_names, eletri_used = [], []
    for row in reader:
        country_names.append(row[0])     # 国家名
        used = row[-5]                   # 电的使用量
        if not used:
            used = 0                     # 没有记录的赋值为 0
        eletri_used.append(int(float(used)))

##########################################################################################
# 用柱状图可视化数据
##########################################################################################
"""
import matplotlib.pyplot as plt

# 只绘制最大用电量前二十个国家, 按用量降序排
top20 = sorted(zip(country_names, eletri_used), key=(lambda atuple: atuple[1]), reverse=True)[:20]
top20_names, top20_used = [], []
for atuple in top20:
    top20_names.append(atuple[0])
    top20_used.append(atuple[1])

plt.figure(figsize=(10, 6), dpi=96)
plt.bar(top20_names, top20_used, facecolor='red', edgecolor='green')
plt.title(title, fontsize=24)
plt.xlabel('Countries', fontsize=16)
plt.ylabel('The Power Using In 1014')
plt.xticks(rotation=45)                # 倾斜45
plt.show()
"""

##########################################################################################
# 用世界地图可视化数据
##########################################################################################
import pygal
from pygal.maps.world import World
from countries import get_country_code
from pygal.style import RotateStyle, LightColorizedStyle

# 根据用电量的范围分组, 统计数据到{国别码: 用电量}6个字典里
group1, group2, group3, group4, group5, group6 = {}, {}, {}, {}, {}, {}
for name, used in zip(country_names, eletri_used):
    code = get_country_code(name)
    if used > 20000:
        group1[code] = used
    elif used > 8000:
        group2[code] = used
    elif used > 3000:
        group3[code] = used
    elif used > 500:
        group4[code] = used
    elif used != 0 :
        group5[code] = used
    else:
        group6[code] = used

# 着色,加亮颜色主题
wm_style = RotateStyle('#336699', base_style=LightColorizedStyle)
wm = World(style=wm_style)
wm.title = title
wm.add('>20th', group1)
wm.add('20th-8th', group2)
wm.add('3th-8th', group3)
wm.add('0.5th-3th', group4)
wm.add('0-0.5th', group5)
wm.add('0', group6)
wm.render_to_file('power_used.svg')
