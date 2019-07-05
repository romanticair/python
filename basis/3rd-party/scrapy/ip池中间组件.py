# 下载中间件
# 导入随机数模块，目的是随机挑选一个IP池中的IP
import random
# 从settings文件(myfirstpjt.settings)中导入设置好的IPPOOL
from myfirstpjt.settings import IPPOOL
# 导入官方文档中HttpProxyMiddleware对应的模块
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

class IPPOOLS(HttpProxyMiddleware):
    def __init__(self, ip=""):
        self.ip = ip
    
    # process_request()方法,主要进行请求处理
    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        print("当前使用的IP是: " + thisip["ipaddr"])
        # 将对应的IP实际添加为具体的代理，用该IP进行爬取
        request.meta["proxy"] = "http://" + thisip["ipaddr"]
