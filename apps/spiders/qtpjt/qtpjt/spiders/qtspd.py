# -*- coding: utf-8 -*-
import scrapy
import re
from qtpjt.items import QtpjtItem
from scrapy.http import Request


class QtspdSpider(scrapy.Spider):
    name = 'qtspd'
    allowed_domains = ['58pic.com']
    start_urls = ['http://58pic.com/tb/']

    def parse(self, response):
        item = QtpjtItem()
        # 构建提取原图网址的正则表达式,截取前半部分
        paturl = '(http://pic.qiantucdn.com/58pic/.*?.jpg)'
        # 得到缩略图链接列表,即无'.jpg!qt324'
        item['picid'] = item['picurl'] = re.compile(paturl).findall(str(response.body))
        yield item
        # 通过for循环一次遍历1到10页图片列表页
        for i in range(1, 10):
            # 构造出下一页图片列表页的网址
            nexturl = 'http://www.58pic.com/piccate/3-0-0-default-0_2_0_0_default_0-%s.html' % i
            yield Request(nexturl, callback=self.parse)
