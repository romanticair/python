"""制作世界地图"""
from pygal.maps.world import World

wm = World()    # 呈现各国数据的世界地图
wm.title = 'North, Central, and South America'
# 要突出的国家的国别码列表
wm.add('North America', ['ca', 'mx', 'us'])
# 而且每次调用add都为指定的国家选择一种新颜色
wm.add('South America', ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'gf',
                         'gy', 'pe', 'py', 'sr', 'uy', 've'])
wm.render_to_file('americas.svg')
