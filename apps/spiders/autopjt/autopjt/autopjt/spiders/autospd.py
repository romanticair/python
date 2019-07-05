# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem
from scrapy.http import Request


class AutospdSpider(scrapy.Spider):
    name = 'autospd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cid10010584.html']

    def parse(self, response):
        item = AutopjtItem()
        # 通过各XPath表达式分别提取商品的名称、价格、链接、评论数等信息
        item['name'] = response.xpath('//a[@class="pic"]/@title').extract()
        item['price'] = response.xpath('//span[@class="price_n"]/text()').extract()
        item['link'] = response.xpath('//a[@class="pic"]/@href').extract()
        item['comnum'] = response.xpath('//a[@id="comm_num_down"]/text()').extract()
        # 提取完后返回item
        yield item
        # 接下来很关键,通过循环自动爬取75页的数据
        for i in range(1, 76):
            # 通过上面总结的网址格式构造要爬取的网址
            url = 'http://category.dangdang.com/pg%s-cid10010584.html' % i
            # 通过yield返回Request, 并指定要爬取的网址和回调函数,实现自动爬取
            yield Request(url, callback=self.parse)
