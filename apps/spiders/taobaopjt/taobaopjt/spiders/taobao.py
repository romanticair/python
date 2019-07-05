# -*- coding: utf-8 -*-
import re
import scrapy
import urllib.request
from scrapy.http import Request
from taobaopjt.items import TaobaopjtItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    # start_urls = ['http://taobao.com/']

    def start_requests(self):
        # 模拟浏览器
        yield Request('https://s.taobao.com/list?spm=a21bo.2017.201867-links-0.38.5af'
                      '911d96nyLwn&q=T%E6%81%A4&cat=50344007&style=grid&seller_type=taobao',
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0'
                                             ') Gecko/20100101 Firefox/61.0'})

    def parse(self, response):
        item = TaobaopjtItem()
        # 提取宝贝链接
        item['url'] = response.xpath('//div[@class="pic"]/a[@class="pic-link"]/@href').extract()
        # 宝贝标题描述
        item['title'] = response.xpath('//img[@class="J_ItemPic img"]/@alt').extract()
        # 宝贝宣传图链接
        item['img_url'] = response.xpath('//img[@class="J_ItemPic img"]/@src').extract()
        print(item['url'], item['title'], item['img_url'])
        yield item
