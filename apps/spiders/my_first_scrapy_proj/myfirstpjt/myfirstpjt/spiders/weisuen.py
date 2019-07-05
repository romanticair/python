# -*- coding: utf-8 -*-
import scrapy

from myfirstpjt.items import MyfirstpjtItem


class WeisuenSpider(scrapy.Spider):
    name = 'weisuen'
    # 允许的域名
    allowed_domains = ['sina.com.cn']
    # 爬取起始网址
    start_urls = ['http://slide.news.sina.com.cn/s/slide_1_2841_103185.html',
                  'http://slide.mil.news.sina.com.cn/k/slide_8_193_45192.html#p=1',
                  ]
    # 定义新属性
    urls = ('http://www.jd.com',
            'http://sina.com.cn',
            'http://yum.iqianyue.com')

    # 重写初始化
    # def __init__(self, myurl=None, *args, **kwargs):
    #     super(WeisuenSpider, self).__init__(*args, **kwargs)
        # 输出要爬的网址，对应值为接受到的参数
        # print('要爬的网址为: %s' % myurl)
        # 重写定义start_urls属性,属性值为传进来的参数值
        # 可在命令行里通过 scrapy crawl weisuen -a myurl='http://...'指定
        # self.start_urls = ["%s" % myurl]
        # 多参数(多个要爬取url)，以'|'切割
        # myurllist = myurl.split('|')
        # self.start_urls = myurllist

    def start_requests(self):
        # 重写该方法,使其将起始地址设置为从urls中读取
        for url in self.urls:
            # 调用默认 make_requests_from_url()方法生成请求
            yield self.make_requests_from_url(url)

    def parse(self, response):
        # pass
        item = MyfirstpjtItem()
        # item['urlname'] = response.xpath('/html/head/title/text()')
        # print(item['urlname'])

        item['title'] = response.xpath('/html/head/title/text()').extract()
        print(item['title'])
        # 如果用json存储多条数据的话
        # item['key'] = response.xpath('//meta[@name="keyword"]/@content').extract()

