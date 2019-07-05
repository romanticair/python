import urllib.request

file = urllib.request.urlopen("http://www.baidu.com")
# urllib.request.urlretrieve(url, filename = 本机文件地址) 直接将对应信息写入本地文件

# data = file.read()
# dataline = file.readline()

# filehandle = open("test.html", 'wb')
# filehandle.write(data)
# filehandle.close()

# filename = urllib.request.urlretrieve("http://edu.51cto.com", filename = "t.html")
# urllib.request.urlcleanup() 清除Urlretrieve执行所造成的缓存
# print(filename)

# 想要获取当前环境信息
# 爬取的网页.info()   如上 file.info()

# 获取当前爬取页面的状态码, 200正确
# file.getcode()

# file.geturl()  http://www.baidu.com"

# urllib.request.quote("url") 不符合URL标准, 需对网址进行编码
# urllib.request.unquote("url") 相应解码

# 浏览器的模拟 - Headers属性:(攻反爬手段) 两种

url = "http://blog.csdn.net/weiwei_pig/article/details/51178226"
file = urllib.request.urlopen(url)
# 403错误  : 禁止访问
# 模拟浏览器可以设置User-Agent信息

# 1: build_opener() 修改报头
headers = ("User-Agent","在Network截取的Headers")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data = opener.open(url).read()

# 2: 使用add_header() 添加报头
# urllib.request.Request().add_header()
req = urllib.request.Request(url)
req.add_header("User-Agent", "在Network截取的Headers")
data = urllib.request.urlopen(req).read()

# urllib.request.urlopen(url, timeout = 10)  10s










