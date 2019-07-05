import urllib.request

"""
 代理服务器地址
 http://yum.iqianyue.com/proxy
"""

# GET, POST, PUT, DELETE, HEAD, OPTIONS 请求
# GET POST 用得较多


# GET 请求:

# 百度hello单词
# https://www.baidu.com/s?if=utf-8&wd=hello&tn=870141_dg
# if=utf-8代表编码信息, wd=hello为字段
# 可简化为https://www.baidu.com/s?wd=hello

# 通过分析这个规律, 通过构造GET请求, 实现自动化爬虫

keywd = "hello"
url = "http://www.baidu.com/s?wd=" + keywd
req = urllib.request.Request(url)
data = urllib.request.urlopen(req).read()
fhandle = open("1.html", "wb")
fhandle.write(data)
fhandle.close()

# 如果关键字需要编码如: 汉字
"""
key = "计算机"
key_code = urllib.request.quote(key)
url_all = url + key_code
req = urllib.request.Request(url_all)
data = urllib.request.urlopen(req).read()
fhandle = open("1.html", "wb")
fhandle.write(data)
fhandle.close()

1. 构建URL地址, 包含GET请求的字段名和字段内容, 满足格式, http://网址?字段名1=字段内容1&字段名2=字段内容2
2. 以URL为参数, 构建Requset对象
3 .通过urlopen()打开Request对象
4. 按需求进行后续处理, 读写 - - - -

"""
# GET 请求 #



# POST请求:(大多数表单)

"""
1. 设置好URL地址
2. 构建表单数据, 使用urllib.request.urlencode对数据进行编码处理
3. 创建Request对象, 参数包括URL和传递的数据
4. 用add_header()添加头信息, 模拟浏览器进行爬取
5. 用urllib.request.urlopen()打开Request对象
6. 后续处理, 读写 - - - -
   属性值
   {字段名1: 字段值1, 字段名2: 字段2, ...}

"""

import urllib.parse

url = 'http://www.iqianyue.com/mypost/'
postdata = urllib.parse.urlencode({
    "name": "ceo@iqianyue.com",
    "pass": "aA123456"}).encode('utf-8')    # urlencode编码处理后, encode为utf-8编码

req = urllib.request.Request(url, postdata)
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")

# req.add_header("User-Agent", "Networks下的信息")
data = urllib.request.urlopen(req).read()
filehandle = open("2.html", 'wb')
filehandle.write(data)
filehandle.close()

# 代理服务器地址
# 如IP:202.75.210.45, 对应端口号7777
# 完整格式: 网址:端口号 即 202.75.210.45:7777

def use_proxy(proxy_addr, url):
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('uft-8')
    return data

proxy_addr = "202.75.210.45:7777"
data = use_proxy(proxy_addr, "http://baidu.com")
print(len(data))


# 开启DebugLog模式:

httphd = urllib.request.HTTPHandler(debuglevel = 1) # 开启
httpshd = urllib.request.HTTPSHandler(debuglevel = 1) # 开启
opener = urllib.request.build_opener(httphd, httpshd) # 创建自定义对象
urllib.request.install_opener(opener) # 创建全局默认opener对象
data = urllib.request.urlopen("http://edu.51cto.com")









