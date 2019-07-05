# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TaobaopjtPipeline(object):
    # def __init__(self):
    #     self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='rootpassword',
    #                                 db='taobao', charset='utf8', use_unicode=True)
    #     self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # for i in range(len(item['comment_nums'])):
        #     try:
        #         comment = item['comments'][i]
        #         sql = 'INSERT INTO taobao(comment) VALUES(comment)'
        #         self.cursor.execute(sql)
        #     except Exception as e:
        #         print(e)
        #
        # self.conn.commit()
        return item

    # def close_spider(self, spider):
    #     self.conn.close()