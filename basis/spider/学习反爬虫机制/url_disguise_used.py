import urllib.request
import http.cookiejar

# 案例2
# 伪装处理
# 设置Headers时, 通过为opener.addheaders添加信息
# 格式: [(字段名1, 对应值1), (字段名2, 对应值2), ...(字段名n, 对呀值n)]

url = "http://news.163.com/16/0825/09/BVA8A9U500014SEH.html"
# 以字典形式设置headers
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0",
           "Connection": "keep-alive",
           "referer": "http://www.163.com/"}

# 设置cookie
cjar = http.cookiejar.CookieJar()
proxy = urllib.request.ProxyHandler({"http": "127.0.0.1:8888"})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler, urllib.request.HTTPCookieProcessor(cjar))

# 建立空列表, 为了以字典格式存储头信息
headAll = []
# 通过for循环遍历字典, 构造出指定格式的headers信息
for key, value in headers.items():
    item = (key, value)
    headAll.append(item)

# 将指定格式的headers信息添加好
opener.addheaders = headAll
urllib.request.install_opener(opener)
data = urllib.request.urlopen(url).read()
fhandle = open("undisTest2.html", "wb")
fhandle.write(data)
fhandle.close()


# "Accept-Encoding" 设置为gzip, deflate可能出现乱码.
# 改进方案
# 注意, 如果通过fiddler调试, 则下方网站要设置要"http://www.baidu.com/, referer字段值也是"
url = "http://www.baidu.com"
headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8",
           "Accept-Encoding": "gb2312, utf-8",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0",
           "Connection": "keep-alive",
           "referer": "http://www.163.com"}

cjar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPHandler, urllib.request.HTTPCookieProcessor(cjar))
headAll = []

for key, value in headers.items():
    item = (key, value)
    headAll.append(item)

opener.addheaders = headAll
urllib.request.install_opener(opener)
data = urllib.request.urlopen(url).read()
fhandle = open("undisTest2.html", "wb")
fhandle.write(data)
fhandle.close()

"""
实践项目中, 要伪装成浏览器, 我们不一定要讲Fiddler设置为代理服务器,
上面案例设置Fiddler是为代理服务器方便抓包, 和调试, 实际项目中可将
该过程省略.

"""





























