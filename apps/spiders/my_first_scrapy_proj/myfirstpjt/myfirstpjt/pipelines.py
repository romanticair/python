# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
# 导入codecs模块，使用其直接进行解码


class MyfirstpjtPipeline(object):
    # def
    # def __init__(self):
    #     # 首先以写入的方式创建或打开一个普通文件用于存储爬取到的数据
    #     self.file = codecs.open('../mydata.txt', 'wb', encoding='utf-8')

    def open_spider(self):
        self.file = codecs.open('../mydata.txt', 'wb', encoding='utf-8')

    # process_item() 为pipelines中的主要处理方法,默认会自动调用
    def process_item(self, item, spider):
        # 设置每行要写的内容
        l = str(item['title']) + '\n'
        # 此处通过print()输出,方便程序的调试
        print(l + '-- been here.')
        # 将对应信息写入文件中
        self.file.write(l)
        # 如果是中文json结构的话,要指定False
        # json.jumps(dict(item), ensure_ascii=False)
        return item

    # close_spider()方法一般在关闭蜘蛛时才调用
    def close_spider(self, spider):
        # 关闭文件,有始有终
        self.file.close()
