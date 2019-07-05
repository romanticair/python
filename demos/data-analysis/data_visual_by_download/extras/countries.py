"""制作世界人口地图前，先获取两个字母的国别码"""
from pygal.maps.world import COUNTRIES


def get_country_code(country_name):
    """根据指定的国家，返回Pygal使用的两个字母的国别码"""
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code

    return None
