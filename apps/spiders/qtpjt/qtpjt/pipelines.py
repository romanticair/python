# -*- coding: utf-8 -*-
import urllib.request
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QtpjtPipeline(object):
    def process_item(self, item, spider):
        # 一个图片列表页中有多张图片，通过for循环一次将图片存储到本地
        for i in range(0, len(item["picurl"])):
            thispic = item["picurl"][i]
            # 根据上面总结的规律构造出原图的url地址
            trueurl = thispic + '!qt324'
            # 构造出图片在本地存储的地址,注意非法路径
            localpath = r"L:/MyPythonProgr/SomePythonProjects/AboutSpider/qtpjt/images/" + item["picid"][i][31:].replace('/', '_')
            # 通过urllib.request.urlretrieve()将原图片下载到本地
            urllib.request.urlretrieve(trueurl, filename=localpath)
        return item
