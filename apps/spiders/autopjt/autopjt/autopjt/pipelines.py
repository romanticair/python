# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class AutopjtPipeline(object):
    def __init__(self):
        # 打开mydata.json文件
        # self.file = codecs.open('L:\MyPythonProgr\SomePythonProjects\\autopjt\mydata.json',
        #                         'wb', encoding='utf-8')
        self.file = codecs.open('L:\MyPythonProgr\SomePythonProjects\\autopjt\mydata2.json',
                            'wb', encoding='utf-8')

    def process_item(self, item, spider):
        # i = json.dumps(dict(item), ensure_ascii=False)
        # line = i + '\n'
        # self.file.write(line)

        # 改一下数据的存储结构,用mydata2.txt存储
        for j in range(0, len(item['name'])):
            # 将当前页的第j个商品的名称复制给变量name
            name = item['name'][j]
            price = item['price'][j]
            comnum = item['comnum'][j]
            link = item['link'][j]
            # 将当前页下第j个商品的信息处理(重整成一字典)
            goods = {'name': name, 'price': price, 'comnum': comnum, 'link': link}
            # 将组合后的数据写入json文件
            line = json.dumps(goods, ensure_ascii=False) + '\n'
            self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
