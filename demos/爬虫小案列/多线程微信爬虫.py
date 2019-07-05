import re
import urllib.request
import time
import urllib.error
import queue
import threading


# 实现思路:

"""
1.将此项目划分为3个线程
2.线程1专门获取对应网址并处理真实网址, 然后写入队列urlqueue中,
  该队列专存放具体文章网址
3.线程2与线程1并行执行, 从线程1提供的文章网址一次爬取信息并处理,
  以及将结果写入本地文件
4. 线程3主要用于判断程序是否完成, 即是实现总体控制

"""

listurl = []

# 使用代理服务器
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


# 线程1, 专门获取对应网址并处理为真实网址
class GetUrl(threading.Thread):
    def __init__(self, key, pagestart, pageend, proxy, urlqueue):
        threading.Thread.__init__(self)
        self.pageStart = pagestart
        self.pageEnd = pageend
        self.proxy = proxy
        self.urlQueue = urlqueue
        self.key = key

    def run(self):
        page = self.pageStart
        # 编码关键词key
        keycode = urllib.request.quote(self.key)
        # 编码 "&page"
        pagecode = urllib.request.quote("&page")

        # 循环爬取各页的文章链接
        for page in range(self.pageStart, self.pageEnd + 1):
            # 分别构建各页的url链接
            url = "http://weixin.sogou.com/weixin?query=" + keycode + "&type=2" + pagecode + str(page)
            # 用代理服务器爬取, 解决IP被封杀问题
            data = use_proxy(self.proxy, url)
            # 列表页正则
            listurlpat = '<div class="txt-box">.*?(http://.*?)"'
            listurl.append(re.compile(listurlpat, re.S).findall(data))
        # 便于测试
        print("共获取到" + str(len(listurl)) + "页")

        for i in range(0, len(listurl)):
            # 等线程2, 合理分配资源
            time.sleep(7)
            for j in range(0, len(listurl[i])):
                try:
                    url = listurl[i][j]
                    # 处理真实url, 读者亦可以分析其它网址的规律, 而这采集网址比真实的多了一串amp;
                    url = url.replace("amp;", "")
                    print("第" + "i" + str(i + 1)  + "j" + str(j + 1) + "次入列")
                    self.urlQueue.put(url)
                    self.urlQueue.task_done()
                except urllib.error.URLError as e:
                    if hasattr(e, "code"):
                        print(e.code)
                    if hasattr(e, "reason"):
                        print(e.reason)
                    time.sleep(10)
                except Exception as e:
                    print("exception:" + str(e))
                    time.sleep(1)

# 线程2, 与线程1并行指向, 从线程1提供的文章网址中一次爬取对应文章信息并处理
class GetContent(threading.Thread):
    def __init__(self, urlqueue, proxy):
        threading.Thread.__init__(self)
        self.urlQuene = urlqueue
        self.proxy = proxy

    def run(self):
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

        fh = open(r"L:\scrapyTestResults\1.html", "ab")
        i = 1
        while True:
            try:
                url = self.urlQuene.get()
                data = use_proxy(self.proxy, url)
                # 文章标题正则
                titlepat = "<title>(.*?)</title>"
                # 文章内容正则
                contentpat = 'id="js_content">(.*?)id="js_sg_bar"'
                # 处理标题
                title = re.compile(titlepat).findall(data)
                # 处理内容
                content = re.compile(contentpat).findall(data)
                # 初始化标题与内容
                thistitle = "此次没有获取到"
                thiscontent = "此次没有获取到"
                # 若标题、内容列表不空, 说明找到了标题, 取列表第0个元素, 赋值给thisTitle
                if (title != []):
                    thistitle = title[0]
                if (content != []):
                    thiscontent = content[0]

                # 将标题与内容汇总给变量dataAll
                dataAll = "<p>标题为:" + thistitle + "</p><p>内容为:" + thiscontent + "</p><br>"
                # 将该篇文章的标题与内容的总信息写入对应文件
                fh.write(dataAll.encode("utf-8"))
                print("第" + str(i) + "个网页第次处理")  # 便于测试
                i += 1

            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                    time.sleep(10)
            except Exception as e:
                print("exception:" + str(e))
                time.sleep(1)

        fh.close()
        # 设置并写入本地文件的html后面的结束部分代码
        htmlLast = '''</body>
    </html>
        '''
        fh = open(r"L:\scrapyTestResults\1.html", "ab")
        fh.write(htmlLast.encode('utf-8'))
        fh.close()


class Control(threading.Thread):
    def __init__(self, urlqueue):
        threading.Thread.__init__(self)
        self.urlQueue = urlqueue

    def run(self):
        while True:
            print("Processing...")
            time.sleep(60)
            if self.urlQueue.empty():
                print("Work done !")
                exit()


if __name__ == '__main__':
    # 模拟浏览器
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    # 将headers安装为全局
    urllib.request.install_opener(opener)

    # 创建一个url队列
    urlQueue = queue.Queue()

    # 关键词
    key = "人工智能"
    # 设置代理服务器, 该代理服务器有可能失效, 读者需自行更换
    proxy = "61.155.164.111:3128"

    # 起始页
    pageStart = 1
    # 爬取到哪页
    pageEnd = 2

    # 创建线程1对象, 随后启动线程1
    t1 = GetUrl(key, pageStart, pageEnd, proxy, urlQueue)
    t1.start()

    # 创建线程2对象, 随后启动线程2
    t2 = GetContent(urlQueue, proxy)
    t2.start()

    # 创建线程3对象, 随后启动线程3
    t1 = Control(urlQueue)
    t1.start()