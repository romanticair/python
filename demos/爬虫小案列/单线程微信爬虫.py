import re
import urllib.request
import time
import urllib.error


# 自定义函数, 功能使用代理服务器
def use_proxy(proxy_addr, url):
    # 建立异常处理机制
    try:
        proxy = urllib.request.ProxyHandler({'http':proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        # 出现URLError异常, 延时10s
        time.sleep(10)
    except Exception as e:
        print("exception:" + str(e))
        # 其它原因, 延时1s
        time.sleep(1)

# 获取所有文章链接
def get_list_url(key, pageStart, pageEnd, proxy):
    page = pageStart
    listUrl = []
    try:
        # 编码关键词key
        keyCode = urllib.request.quote(key)
        # 编码 "&page="
        pageCode = urllib.request.quote("&page=")

        # 循环爬取各页的文章链接
        for page in range(pageStart, pageEnd + 1):
            # 分别构建各页的url链接
            url = "http://weixin.sogou.com/weixin?query=" + keyCode + "&type=2" + pageCode + str(page)
            # 用代理服务器爬取, 解决IP被封杀问题
            data = use_proxy(proxy, url)
            print(data)
            # 获取文章链接的正则表达式
            listUrlPat = '<div class="txt-box">.*?(http://.*?)"'
            # 获取每页的所有文章链接并添加到列表listUrl中
            listUrl.append(re.compile(listUrlPat, re.S).findall(data))

        print("共获取到" + str(len(listUrl)) + "页") # 便于测试
        return listUrl
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        # 出现URLError异常, 延时10s
        time.sleep(10)
    except Exception as e:
        print("exception:" + str(e))
        # 其它原因, 延时1s
        time.sleep(1)

# 通过文章链接获取对应内容
def get_content(listUrl, proxy):
    i = 0
    # 设置本地文件中的开始Html编码
    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.O Transitional//EN" "http://
    www.w3.org/TR/xhtml1/DTD/xhtm1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>微信文章页面</title>
    </head>
    <body>'''

    fh = open(r"L:\scrapyTestResults\1.html", "wb")
    fh.write(html.encode("utf-8"))
    fh.close()

    # 再次以追加写入的方式打开文件, 以写入对应文章内容
    fh = open(r"L:\scrapyTestResults\1.html", "ab")
    # 此时listUrl为二维列表, 第一维存的信息和第几页相关, 第二维存的和第几个文章链接相关

    for i in range(0, len(listUrl)):
        for j in range(0, len(listUrl[i])):
            try:
                url = listUrl[i][j]
                # 处理真实url, 读者亦可以分析其它网址的规律, 而这采集网址比真实的多了一串amp;
                url = url.replace("amp;", "")
                # 使用代理爬取对应网址内容
                data = use_proxy(proxy, url)
                # 文章标题正则表达式
                titlePat = "<title>(.*?)</title>"
                # 文章内容正则表达式
                contentPat = 'id="js_content">(.*?)id="js_sg_bar"'

                # 处理标题
                title = re.compile(titlePat).findall(data)
                # 处理内容
                content = re.compile(contentPat).findall(data)

                # 初始化标题与内容
                thisTitle = "此次没有获取到"
                thisContent = "此次没有获取到"
                # 若标题、内容列表不空, 说明找到了标题, 取列表第0个元素, 赋值给thishTitle
                if (title != []):
                    thisTitle = title[0]
                if (content != []):
                    thisContent = content[0]

                # 将标题与内容汇总给变量dataAll
                dataAll = "<p>标题为:" + thisTitle + "</p><p>内容为:" + thisContent + "</p><br>"
                # 将该篇文章的标题与内容的总信息写入对应文件
                fh.write(dataAll.encode("utf-8"))
                print("第" + str(i + 1) + "个网页第" + str(j + 1) + "次处理") # 便于测试

            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                # 出现URLError异常, 延时10s
                time.sleep(10)
            except Exception as e:
                print("exception:" + str(e))
                # 其它原因, 延时1s
                time.sleep(1)

    fh.close()
    # 设置并写入本地文件的html后面的结束部分代码
    htmlLast = '''</body>
    </html>
    '''
    fh = open(r"L:\scrapyTestResults\1.html", "ab")
    fh.write(htmlLast.encode('utf-8'))
    fh.close()

if __name__ == '__main__':
    # 模拟浏览器
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    # 将headers安装为全局
    urllib.request.install_opener(opener)

    # 设置一个列表listUrl存储文章网址列表
    # 关键词
    key = "物联网"
    # 设置代理服务器, 该代理服务器有可能失效, 读者需自行更换
    proxy = "61.155.164.111:3128"
    # Ps:可以为get_list_url()与get_content()设置不同的代理服务器

    # 起始页
    pageStart = 1
    # 爬取到哪页
    pageEnd = 3
    listUrl = get_list_url(key, pageStart, pageEnd, proxy)
    get_content(listUrl, proxy)







