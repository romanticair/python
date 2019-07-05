import re
import urllib.request


"""
把一个网页中所有链接地址提取出来
For test
author:
email:
"""

# 实现思路:
# 1) 确定要爬取的入口链接
# 2) 根据需求构建好链接提取的正则表达式
# 3) 模拟成浏览器并爬取对应网页
# 4) 根据 2) 中表达式提取出网页中包含的链接
# 5) 过滤重复链接
# 6) 后续操作

def getlink(url):
    # 模拟浏览器
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]

    # 安装opener为全局
    urllib.request.install_opener(opener)
    file = urllib.request.urlopen(url)
    data = str(file.read())

    # 根据需求构建好链接表达式
    pattern = '(https?://[^\s)";]+.(\w|/)*)'
    link = re.compile(pattern).findall(data)

    # 去重
    link = list(set(link))
    return link

if __name__ == '__main__':
    # 要爬取的网页链接
    url = "http://blog.csdn.net"
    # 获取对应页面中包含的链接地址
    linklist = getlink(url)
    # 通过for循环分别遍历输出获取到的链接
    for link in linklist:
        print(link[0])


















