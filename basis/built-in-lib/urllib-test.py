"""
urllib的request模块可以非常方便地抓取URL内容，也就是发送一个GET请求
到指定的页面，然后返回HTTP的响应
"""
from urllib import request, parse
import urllib
import json

# 例如，对豆瓣的一个 url 进行抓取，并返回响应
with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' %(k, v))

    print('Data:', data.decode('utf-8'))

# 想模拟浏览器发送 GET 请求，就需要使用Request对象，通过往Request对象
# 添加HTTP头，就可以把请求伪装成浏览器
# 例如，模拟iPhone 6去请求豆瓣首页
req = request.Request('http://www.douban.com/')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))

# 如果要以 POST 发送请求，只需要把参数data以bytes形式传入
# 模拟一个微博登录，先读取登录的邮箱和口令，然后按照 weibo.cn 的
# 登录页的格式以username=xxx&password=xxx的编码传入
print('Login to weibo.cn...')
email = input('Email: ')
passwd = input('Password: ')
login_data = parse.urlencode([
    ('username', email),
    ('password', passwd),
    ('entry', 'mweibo'),
    ('client_id', ''),
    ('savestate', '1'),
    ('ec', ''),
    ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
])

req = request.Request('https://passport.weibo.cn/sso/login')
req.add_header('Origin', 'https://passport.weibo.cn')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) Apple'
                             'WebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res='
                          'wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

with request.urlopen(req, data=login_data.encode('utf-8')) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))

# 如果还需要更复杂的控制，比如通过一个 Proxy 去访问网站，需要
# 利用ProxyHandler来处理
proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
with opener.open('http://www.example.com/login.html') as f:
    pass


def fetch_data(url):
    """利用urllib读取JSON，然后将JSON解析为Python对象"""
    with urllib.request.urlopen(url) as f:
        # 反序列化即为python对象
        return json.loads(f.read().decode('utf-8'))

# 测试
URL = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json'
data = fetch_data(URL)
print(data)
assert data['query']['results']['channel']['location']['city'] == 'Beijing'
print('ok')
