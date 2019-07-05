import re
import urllib.request
import urllib.error
import time

"""
爬取京东手机图片
test for scrapy
author:
email:

"""

# GET 请求
def craw(url, page):
    html = urllib.request.urlopen(url).read()
    html = str(html)
    pat1 = '<div id="plist".+? <div class="page clearfix">'  # 过滤后的第一部分
    result1 = re.compile(pat1).findall(html)
    result1 = result1[0]

    pat2 = '<img width="220" height="220" data-img="1" src="(.+?.jpg)">'
    imageList = re.compile(pat2).findall(result1)
    x = 1

    for imageUrl in imageList:
        imageFileName = "L:\scrapyTestResults\imageGetting\\" + str(page) + str(x) + ".jpg"
        imageUrl = "https:" + imageUrl
        try:
            urllib.request.urlretrieve(imageUrl, filename = imageFileName)
            time.sleep(1)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                x += 1
            if hasattr(e, "reason"):
                x += 1
        x += 1

if __name__ == '__main__':
    for i in range(1, 20):
        url = "https://list.jd.com/list.html?cat=9987,653,655&page=" + str(i)
        craw(url, i)

