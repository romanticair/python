import unittest
from countries import get_country_code


class CountriesTestCase(unittest.TestCase):
    """单元测试 - countries.py"""

    def test_all_countries_code(self):
        """能够成功获取全部国家的国别码吗?"""
        code1 = get_country_code('Andorra')
        code2 = get_country_code('United Arab Emirates')
        self.assertEqual([code1, code2], ['ad', 'ae'])


if __name__ == '__main__':
    unittest.main()
