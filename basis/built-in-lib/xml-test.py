"""
操作XML有两种方法：DOM和SAX。DOM会把整个XML读入内存，解析为树，因此占用内存大，
解析慢，优点是可以任意遍历树的节点。SAX是流模式，边读边解析，占用内存小，解析快，
缺点是我们需要自己处理事件
正常情况下，优先考虑SAX，因为DOM实在太占内存

Python中使用SAX解析XML非常简洁，通常我们关心的事件是start_element，end_element和
char_data，准备好这3个函数，然后就可以解析xml了

举个例子，当SAX解析器读到一个节点时：
<a href="/">python</a>

会产生3个事件：

1.start_element事件，在读取<a href="/">时；
2.char_data事件，在读取python时；
3.end_element事件，在读取</a>时。
"""
from xml.parsers.expat import ParserCreate
from urllib import request
import time


class DefaultSaxHandler(object):
    # 实验一下
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)

# 需要注意的是读取一大段字符串时，CharacterDataHandler可能被多次调用，
# 所以需要自己保存起来，在 EndElementHandler 里面再合并
# 最简单也是最有效的生成XML的方法是拼接字符串

# 解析XML时，注意找出自己感兴趣的节点，响应事件时，把节点数据保存起来。解析完毕后，就可以处理数据

# 用 SAX 编写程序解析 Yahoo 的 XML 格式的天气预报
# 参数 woeid 是城市代码，要查询某个城市代码，可以在weather.yahoo.com搜索城市，
# 浏览器地址栏的URL就包含城市代码


class DefaultSaxHandler(object):
    def __init__(self):
        self.location = {}
        self.forecast = []

    def start_element(self, name, attrs):
        if name == 'yweather:location':
            self.location = attrs
        if name == 'yweather:forecast':
            data = {}
            date = time.strftime('%Y-%m-%d' , time.strptime(attrs['date'],'%d %b %Y'))
            data['date'] = date
            data['high'] = attrs['high']
            data['low'] = attrs['low']
            self.forecast.append(data)

    def end_element(self, name):
        pass

    def char_data(self, text):
        pass


def parseXml(xml_str):
    handler = DefaultSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml_str)
    return {
        'city': handler.location['city'],
        'forecast': handler.forecast
    }

# 测试:
URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=xml'
with request.urlopen(URL, timeout=4) as f:
    data = f.read()

result = parseXml(data.decode('utf-8'))
print(result)
assert result['city'] == 'Beijing'
print('ok')
