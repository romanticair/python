# 利用 @property 给一个Screen对象加上width和height属性，以及一个只读属性resolution
class Screen(object):
    def __init__(self):
        self.__width = 20
        self.__height = 30
        self.__resolution = 786432

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            raise ValueError('width must be an integer!')
        # if 100 < value:
        #     raise ValueError('width must between 0 - 100!')
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise ValueError('height must be an integer!')
        # if 60 < value :
        #     raise ValueError('height must between 0 - 60!')
        self.__height = value

    @property
    def resolution(self):
        return self.__resolution


# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')
