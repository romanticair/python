import urllib.request

"""
# 是否超时, 1s无响应则为超时
for i in range(1, 100):
    try:
        file = urllib.request.urlopen("http://yun.iqianyue.com", timeout = 1)
        data = file.read()
        print(len(data))
    except Exception as e:
        print("something wrong - ->" + str(e))

"""
"""

def use_proxy(proxy_addr, url):
    # 设置代理服务器信息
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    # 设置全局默认的opener对象
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data

proxy_addr = "112.237.28.190:8118"
data = use_proxy(proxy_addr, "http://www.baidu.com")
print(len(data))

"""
"""

httphd = urllib.request.HTTPHandler(debuglevel = 1) # 开启
httpshd = urllib.request.HTTPSHandler(debuglevel = 1) # 开启
opener = urllib.request.build_opener(httphd, httpshd) # 创建自定义对象
urllib.request.install_opener(opener) # 创建全局默认opener对象
data = urllib.request.urlopen("http://edu.51cto.com")

"""