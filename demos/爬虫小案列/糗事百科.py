import urllib.request
import re


"""
爬取糗事百科上的段子
For test
author:
email:

"""

# 实现思路:
# 精通Python网络爬虫p91

def get_content(url, page):
    # 模拟浏览器
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]

    # 将headers安装为全局
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode("utf-8")

    # 构建对应用户提取的正则表达式
    userPat = '<h2>\n(.*?)\n</h2>'
    # 构建段子内容提取的正则表达式
    contentPat = '<div class="content">\n<span>(.*?)\n</span>'
    # 寻找出所有的用户
    userList = re.compile(userPat, re.S).findall(data)
    # 寻找出所有内容
    contentList = re.compile(contentPat, re.S).findall(data)
    # print(userList)
    # print(contentList)

    x = 1
    # 通过for循环遍历段子内容并将内容赋给对应变量
    for content in contentList:
        content = content.replace("\n", "").replace("<br/>", "")

        # 用字符串作为变量名, 先将对应字符串赋给一个变量
        name = "content" + str(x)
        # 通过exec()实现用字符串作为变量名并赋值
        exec(name + "=content")
        x += 1

    y = 1
    # 通过for循环遍历用户, 并输出该用户对应的内容
    for user in userList:
        name = "content" + str(y)
        print("Page" + str(page) + "用户" + "no." + str(y) + "是:" + user)
        print("内容是: ", end = "")
        exec("print("+name+")")
        print()
        y += 1

if __name__ == '__main__':
    # 分别获取各页的段子, 通过for获取多页
    for i in range(1, 5):
        url = "https://www.qiushibaike.com/8hr/page/" + str(i)
        get_content(url, i)



































