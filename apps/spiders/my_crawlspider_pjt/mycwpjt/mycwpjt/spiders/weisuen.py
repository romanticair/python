# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor  # 链接提取器
from scrapy.spiders import CrawlSpider, Rule

from mycwpjt.items import MycwpjtItem


class WeisuenSpider(CrawlSpider):
    name = 'weisuen'
    allowed_domains = ['sohu.com']
    start_urls = ['http://news.sohu.com/']

    # CrawlSpider可以实现无规律爬取,更通用
    rules = (
        # 新闻网页的URL地址类似于:
        # http://news.sohu.com/20160926/n469167364.shtml
        # 所以可得到提取的正则表达式 '.*?/n.*?shtml'
        Rule(LinkExtractor(allow='.*?/n.*?shtml', allow_domains=('sohu.com',)),
             callback='parse_item', follow=False),
    )

    # 默认的
    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    # 假如想提取链接中有'.shtml'字符串的链接
    # rules = (
    #     Rule(LinkExtractor(allow=r'.shtml'), callback='parse_item', follow=True),
    # )

    # 假如想进一步限制只提取官方链接sohu.com
    # rules = (
    #     Rule(LinkExtractor(allow=r'.shtml'), allowed_domains=('sohu.com'),
    #          callback='parse_item', follow=True),
    # )

    def parse_item(self, response):
        i = MycwpjtItem()
        # 根据XPath表达式提取新闻网页中的标题
        i['name'] = response.xpath('/html/head/title/text()').extract()
        # 根据XPath表达式提取新闻网页中的标题
        i['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
