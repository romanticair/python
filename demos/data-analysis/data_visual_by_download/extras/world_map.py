"""绘制世界地图"""
from pygal.maps.world import COUNTRIES, World


def world_country_map():
    """绘制世界地图"""
    wm_c = World()
    # wm_c.force_url_protocol = 'http'
    wm_c.title = 'World Map'
    for code, name in COUNTRIES.items():
        wm_c.add(name, code)

    wm_c.add('Yemen', {'ye': 'Yemen'})
    wm_c.render_to_file('world_map.svg')

if __name__ == '__main__':
    world_country_map()
