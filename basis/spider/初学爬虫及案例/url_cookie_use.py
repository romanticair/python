import urllib.request
import urllib.parse

# 先进行无Cookie处理登录:
def first():
    url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=Lo9UZ'
    postdata = urllib.parse.urlencode({'username':"weisuen",
                                       'password': 'aA123456'}).encode('utf-8')
    req = urllib.request.Request(url, postdata) # 构建对象
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")

    data = urllib.request.urlopen(req).read() # 登录并爬取网页
    fhandle = open("t1.html", "wb")
    fhandle.write(data)
    fhandle.close()

    url2 = "http://bbs.chinaunix.net" # 设置要爬取的该网站下的其它网址
    req2 = urllib.request.Request(url2, postdata)
    req2.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")

    data2 = urllib.request.urlopen(req2).read() # 爬取该网站下的其它网页
    fhandle = open("t2.html", "wb")
    fhandle.write(data2)
    fhandle.close()

    # 结果是t1.html登录成功, t2.html没有登录



# 进行Cookie处理思路:

"""
1) 导入Cookie处理模块http.cookiejar
2) 用htt.cookiejar.CookieJar()创建CookieJar对象
3) 用HTTPCookieProcessor创建cookie处理器, 并以其为参数构建opener对象
4) 创建全局默认的opener对象

"""
def second():
    import http.cookiejar

    url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=Lo9UZ'
    postdata = urllib.parse.urlencode({'username':"weisuen",
                                       'password': 'aA123456'}).encode('utf-8')

    req = urllib.request.Request(url, postdata) # 构建对象
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")

    # 用http.cookiejar.CookieJar() 创建CookieJar对象
    cjar = http.cookiejar.CookieJar()
    # 用HTTPCookieProcessor创建cookie处理器, 以其作为参数构建opener对象
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    # 将opener安装为全局
    urllib.request.install_opener(opener)
    file = opener.open(req)
    data = file.read()

    file = open("t3.html", "wb")
    file.write(data)
    file.close()

    url2 = "http://bbs.chinaunix.net" # 设置要爬取的该网站下的其它网址
    data2 = urllib.request.urlopen(url2).read()
    fhandle = open("t4.html", "wb")
    fhandle.write(data2)
    fhandle.close()























