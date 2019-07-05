# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaopjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()                 # 宝贝页面链接
    img_url = scrapy.Field()             # 宝贝照片链接
    view_price = scrapy.Field()          # 原价
    price = scrapy.Field()               # 实际价格
    sales = scrapy.Field()               # 付款人数
    title = scrapy.Field()               # 宝贝标题
    paid = scrapy.Field()                # 成功交易量
    favorite_nums = scrapy.Field()       # 人气量
    comment_nums = scrapy.Field()        # 评论数
    good = scrapy.Field()                # 好评
    bad = scrapy.Field()                 # 差评
    addition = scrapy.Field()            # 追评
    middle = scrapy.Field()              # 中评
    comments = scrapy.Field()            # 评论内容
    date = scrapy.Field()                # 评论日期



