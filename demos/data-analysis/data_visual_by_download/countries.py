"""制作世界人口地图前，先获取两个字母的国别码"""
from pygal.maps.world import COUNTRIES              # 国别码字典(key-value为国别码-国家名)

# for country_code in sorted(COUNTRIES.keys()):  # 按字母排序
#     print(country_code, COUNTRIES[country_code])


def get_country_code(country_name):
    """根据指定的国家，返回Pygal使用的两个字母的国别码"""
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    # 若没找到返回None
    return None

# print(get_country_code('Andorra'))
# print(get_country_code('United Arab Emirates'))
# print(get_country_code('Afghanistan'))
