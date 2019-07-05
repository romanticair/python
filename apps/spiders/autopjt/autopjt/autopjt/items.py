# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutopjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 存储商品名,价格,链接,评论数
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    comnum = scrapy.Field()
