import re
import urllib.request
import urllib.error
import time

"""
for: 爬取泸深股票全部代码, 以及历年数据
author:
date:
e-mail:
"""
# 单线程

# 获取全部股票名称及代码
def get_stocks_code(url):
    # 伪装并请求数据
    data = get_data(url)
    shanghai = 'sh\d{6}.html">(.*?)</a>'
    shenzhen = 'sz\d{6}.html">(.*?)</a>'

    shstockcodes = re.compile(shanghai).findall(data) # a list
    szstockcodes = re.compile(shenzhen).findall(data) # a list

    with open("shanghai_stocks_code.csv", 'w') as fhandle:
        for code in shstockcodes:
            fhandle.write(code)

    with open("shenzhen_stocks_code.csv", 'w') as fhandle:
        for code in szstockcodes:
            fhandle.write(code)

    return shstockcodes, szstockcodes


# 获取单只股票历年数据
def get_history_stock_data(url, i, whichstock):
    # 伪装并请求数据
    data = get_data(url)
    # 自定义目录
    # 以csv格式写入
    with open(whichstock + '_stock_' + str(i) + '_data.csv', 'w') as f:
        f.write(data)

# 获取全部股票历年数据
def deal_all_stocks_datas(shanghai, shenzhen):
    # 分别处理上海和深圳股票数据
    # 上海0 深圳1 债券2 开头
    index = 1 # 文件标记
    for code in shanghai:
        if code[-7] in ['1', '5', '2']:
            continue
        date = start_web(code)
        url = stockdataurl('0' + code[-7: -1], date[0], date[1])
        get_history_stock_data(url, index, 'shanghai') # 股票代码6位
        index += 1

    index = 1
    for code in shenzhen:
        if code[-7] in ['1', '5', '2']:
            continue
        date = start_web(code)
        url = stockdataurl('1' + date[-7 : -1], date[0], date[1])
        get_history_stock_data(url, index, 'shenzhen')
        index += 1

def get_data(url):
    try:
        data = urllib.request.urlopen(url).read().decode('gbk')
        return data
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    except urllib.error.HTTPError as e:
        print(e, "HTTP Error 404: Not Found")
    except Exception as e:
        print("exception:" + str(e))

# 获取单只股票的起始时间
def start_web(code):
    start_url = "http://quotes.money.163.com/trade/lsjysj_" + code[-7 : -1] + ".html"
    print(start_url)
    start_end_info = urllib.request.urlopen(start_url).read().decode('utf-8')
    pattern1 = 'name="date_start_type" value="(.*?)" >上市日'
    pattern2 = 'name="date_end_type" value="(.*?)">今日'
    start_date = re.compile(pattern1).findall(start_end_info)
    end_date = re.compile(pattern2).findall(start_end_info)
    print(start_date, end_date)
    return (start_date[0].replace('-', ''), end_date[0].replace('-', ''))

def stockdataurl(code, start, end):
    return ("http://quotes.money.163.com/service/chddata.html?code="+code+'&start='+start+ '&end='+end+
           "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP")

def disguise():
    # 模拟浏览器处理
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)

if __name__ == '__main__':
    # 股票代码网址
    stockcodeurl = 'http://quote.eastmoney.com/stocklist.html'
    # 伪装
    disguise()
    # 获取股票代码, 并分别以列表形式返回
    shenzhen, shanghai = get_stocks_code(stockcodeurl)
    # 获取各只股票代码历年所有数据
    deal_all_stocks_datas(shanghai, shenzhen)



    # 上证股票代码是6开头的，深证股票是0开头或3开头的
    # 基金是1或5开头的





