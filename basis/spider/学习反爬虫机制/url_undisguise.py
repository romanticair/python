import urllib.request
import http.cookiejar

# 案例1
# 测试, 不设置浏览器伪装

url = "http://news.163.com/16/0825/09/BVA8A9U500014SEH.html"
cjar = http.cookiejar.CookieJar()
proxy = urllib.request.ProxyHandler({'http': "127.0.0.1:8888"})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler, urllib.request.HTTPCookieProcessor(cjar))

urllib.request.install_opener(opener)
data = urllib.request.urlopen(url).read()
fhandle = open("undisTest1.html", "wb")
fhandle.write(data)
fhandle.close()

"""
Results:
    GET /16/0825/09/BVA8A9U500014SEH.html HTTP/1.1
    Accept-Encoding: identity
    User-Agent: Python-urllib/3.5
    Host: news.163.com
    Connection: close

"""

