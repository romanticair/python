import time
import re
import urllib.request
import urllib.error
import queue
import threading

"""
for: 爬取泸深股票全部代码, 以及历年数据
author:
date:
e-mail:
"""
# 三线程
# 1.线程1负责获取股票代码, 找出股票历年数据起始时间, 然后获得对应股票数据的url, 写入队列
# 2.线程2负责提取队列的url, 进行下载保存
# 3.线程3负责调度


class GetUrl(threading.Thread):
    """获取股票起始时间, 然后构造Url并写入队列.

    Longer class information....

    Attributes:
        sh: ShangHai's stock code.
        sz: ShenZhen's stock code.
        urlqueue: stocks datas' url queue.
        filequeue: stocks' file queue.
    """
    def __init__(self, sh, sz, urlqueue, filequeue):
        threading.Thread.__init__(self)
        self.urlQueue = urlqueue
        self.fileQueue = filequeue
        self.sh = sh
        self.sz = sz

    # 获取要处理的股票代码 get_code
    def run(self):
        index = 1
        # Deal with sh stocks
        for stock in self.sh:
            if stock[-7] in ['1', '5', '2']:
                continue
            # 获取股票起始日期
            stockDate = self.get_date(stock[-7: -1]) # a tuple with two date
            # 构造url
            url = self.make_url('0' + stock[-7: -1], stockDate[0], stockDate[1])
            # 把股票文件名写入队列
            self.fileQueue.put('shanghai_stock_' + str(index) + '_data.csv')
            # 写入队列
            self.urlQueue.put(url)
            index += 1
            time.sleep(1)

        index = 1
        # Deal with sz stocks
        for stock in self.sz:
            if stock[-7] in ['1', '5', '2']:
                continue
            stockDate = self.get_date(stock[-7: -1])  # a tuple with two date
            url = self.make_url('1'+ stock[-7: -1], stockDate[0], stockDate[1])
            self.fileQueue.put('shenzhen_stock_' + str(index) + '_data.csv')
            self.urlQueue.put(url)
            index += 1
            time.sleep(1)

    # 获取相应股票起始日期, 然后构造url并使其入队列
    def get_date(self, code):
        start_url = "http://quotes.money.163.com/trade/lsjysj_" + code + ".html"
        print(start_url)
        start_end_info = urllib.request.urlopen(start_url).read().decode('utf-8')
        pattern1 = 'name="date_start_type" value="(.*?)" >上市日'
        pattern2 = 'name="date_end_type" value="(.*?)">今日'
        start_date = re.compile(pattern1).findall(start_end_info)
        end_date = re.compile(pattern2).findall(start_end_info)
        print(start_date, end_date)
        return (start_date[0].replace('-', ''), end_date[0].replace('-', ''))

    # 构造相应股票历年数据url
    def make_url(self, code, start, end):
        return ("http://quotes.money.163.com/service/chddata.html?code="+code+'&start='+start+'&end='+end+
                "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP")


class GetContent(threading.Thread):
    """下载历年数据

    在队列取出url, 下载相应数据.

    Attributes:
       urlqueue: stocks datas' url queue.
       filequeue: stocks' file queue.
    """
    def __init__(self, urlqueue, filequeue):
        threading.Thread.__init__(self)
        self.urlQueue = urlqueue
        self.fileQueue = filequeue

    # 提取url, 爬取数据 craw_stock_data
    def run(self):
        while True:
            url = self.urlQueue.get()
            data = self.get_data_safety(url)
            fileName = self.fileQueue.get()
            # 以csv格式写入
            with open(fileName, 'w') as f:
                f.write(data)

    # 带异常处理模式下爬取数据
    def get_data_safety(self, url):
        try:
            return urllib.request.urlopen(url).read().decode('gbk')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        except Exception as e:
            print("exception:" + str(e))


class Control(threading.Thread):
    """Control GetUrl and GetContent thread

    Attributes:
        urlqueue: stocks datas' url queue.
        filequeue: stocks' file queue.
    """
    def __init__(self, urlqueue, filequeue):
        threading.Thread.__init__(self)
        self.urlQueue = urlqueue
        self.fileQueue = filequeue

    def run(self):
        while True:
            print("Processing...")
            time.sleep(30)
            if self.urlQueue.empty():
                print('Work done!')
                exit()


if __name__ == '__main__':
    from get_stocks_code_and_datas1 import get_stocks_code, disguise
    # 导入获取股票代码和模拟浏览器的函数
    # 伪装
    disguise() # 设置代理更安全
    # 分别获取sh, sz的全部股票代码
    sh, sz =  get_stocks_code('http://quote.eastmoney.com/stocklist.html') # two list

    # 创建一个url队列
    urlQueue = queue.Queue()
    # 创建一个stockFile队列
    fileQueue = queue.Queue()
    # 创建线程1对象
    t1 = GetUrl(sh, sz, urlQueue, fileQueue)
    t1.start()
    # 创建线程2对象
    t2 = GetContent(urlQueue, fileQueue)
    t2.start()
    # 创建线程3对象
    t3 = Control(urlQueue, fileQueue)
    t3.start()








