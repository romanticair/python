# -*- coding: utf-8 -*-
import scrapy

# 假如遇到动态加载的数据
import re
import urllib.request
from hexunpjt.items import HexunpjtItem
from scrapy.http import Request


class MyhexunspdSpider(scrapy.Spider):
    name = 'myhexunspd'
    allowed_domains = ['hexun.com']
    # start_urls = ['http://hexun.com/']
    # 设置要爬取的用户的uid，为后续构造爬取网址做准备,可对uid进行设置,爬它用户
    uid = 'shihanbingblog'
    # 通过start_requests方法编写首次的爬取行为

    def start_requests(self):
        # 首次爬取模拟成浏览器进行
        yield Request('http://' + str(self.uid) + '.blog.hexun.com/p1/default.html',
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'})

    def parse(self, response):
        item = HexunpjtItem()
        item['name'] = response.xpath('//span[@class="ArticleTitleText"]/a/text()').extract()
        item['url'] = response.xpath('//span[@class="ArticleTitleText"]/a/@href').extract()
        # content = response.xpath('//div[@class="ArticleSubstanceText"]/text()')
        # 接下来需要使用urllib和re模块获取博文的评论数和阅读数
        # 首先提取存储评论数和点击数网址的正则表达式
        pat1 = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        # hcur1为存储评论数和点击数的网址
        hcur1 = re.compile(pat1).findall(str(response.body))[0]
        # 模拟成浏览器
        headers2 = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/2010010116039659-115975012-115943906-115943904-115926686-115858644-115801649-11 Firefox/61.0')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers2]
        # 将opener安装为全局
        urllib.request.install_opener(opener)
        # data为对应博客列表页的所有博文的点击数与评论数数据
        data = urllib.request.urlopen(hcur1).read()
        # pat2为提取文章阅读数的正则表达式
        pat2 = "click\d*?','(\d*?)'"
        # pat3为提取文章评论数的正则表达式
        pat3 = "comment\d*?','(\d*?)'"
        # 提取文读数和评论数数据并分配
        item['hits'] = re.compile(pat2).findall(str(data))
        item['comment'] = re.compile(pat3).findall(str(data))
        yield item
        # 提取博文列表页的总页数
        pat4 = 'blog.hexun.com/p(.*?)/'
        # 通过正则表达式获取到的数据为一个列表，倒数第二个元素为总页数
        data2 = re.compile(pat4).findall(str(response.body))
        if len(data2) >= 2:
            totalurl = int(data2[-2])
        else:
            totalurl = 1

        for i in range(2, totalurl + 1):
            # 构造下一个要爬取的url
            nexturl = 'http://' + str(self.uid) + '.blog.hexun.com/p%s/default.html' % i
            # 进行下一次爬取,下一次爬取仍然模拟成浏览器进行
            yield Request(nexturl, callback=self.parse,
                          headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'})
