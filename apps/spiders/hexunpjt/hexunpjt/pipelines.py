# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunpjtPipeline(object):
    def __init__(self):
        # 刚开始时连接对应数据库
        self.conn = pymysql.connect(host="localhost", user="root",
                                    passwd="rootpassword", db="hexun",
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 每个博文列表页包含多篇博文的信息，可以通过for循环一次处理各博文的信息
        for j in range(0, len(item["name"])):
            try:
                # 将获取到的name、url、hits、comment分别赋给各变量
                name = item["name"][j]
                url = item["url"][j]
                hits = item["hits"][j]
                comment = item["comment"][j]
                # 构造对应的sql语句，实现将获取到的对呀数据插入数据库中
                sql = "INSERT INTO myhexun(name, url, hits, comment) VALUES('"+name+"','"+url+"','"+hits+"','"+comment+"')"
                # 通过query实现执行对应的sql语句
                # self.conn.query(sql)
                self.cursor.execute(sql)
            except Exception as error:
                print(error)

        self.conn.commit()
        return item

    def close_spider(self, spider):
        # 最后关闭数据库链接
        self.conn.close()
