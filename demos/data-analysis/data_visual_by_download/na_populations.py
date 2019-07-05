"""在世界地图上呈现数字数据"""
from pygal.maps.world import World

wm = World()
wm.title = 'Populations of Countries in North America'
# 练习(传递字典, pygal根据人口值自动分配深浅不一的颜色给不同的国家,浅->深)
wm.add('North America', {'ca': 3412600, 'us': 309349000, 'mx': 113423000})
wm.render_to_file('na_populations.svg')
