"""
将返回的数据插入数据库中，包括建表，插入，关闭等操作。
表中设置了15个字段，用来存储电影信息。
"""

import sqlite3


class DataOutput:
    def __init__(self):
        self.cx = sqlite3.connect('MTime.db')
        self.create_table('MTime')
        self.data = []

    def create_table(self, table_name):
        """
        创建数据表
        :param table_name: 表名称
        :return:
        """
        values = '''
        id INTEGER PRIMARY KEY,
        MovieId INTEGER,
        MovieTitle VARCHAR(40) NOT NULL,
        RatingFinal REAL NOT NULL DEFAULT 0.0,
        ROtherFinal REAL NOT NULL DEFAULT 0.0,
        RPictureFinal REAL NOT NULL DEFAULT 0.0,
        RDirectoryFinal REAL NOT NULL DEFAULT 0.0,
        RStoryFinal REAL NOT NULL DEFAULT 0.0,
        Usercount INTEGER NOT NULL DEFAULT 0,
        AttitudeCount INTEGER NOT NULL DEFAULT 0,
        TotalBoxOffice VARCHAR(20) NOT NULL,
        TodayBoxOffice VARCHAR(20) NOT NULL,
        Rank INTEGER NOT NULL DEFAULT 0,
        ShowDays INTEGER NOT NULL DEFAULT 0,
        isReLease INTEGER NOT NULL,
        '''
        self.cx.execute('CREATE TABLE IF NOT EXISTS %s(%s)' % (table_name, values))

    def store_data(self, data):
        """
        数据存储
        :param data:
        :return:
        """
        if data is None:
            return
        self.data.append(data)
        if len(self.data) > 10:
            self.output_db('MTime')

    def output_db(self, table_name):
        """
        将数据存储到sqlite
        :param table_name:
        :return:
        """
        for data in self.data:
            self.cx.execute("INSERT INTO %s (MovieId, MovieTitle, RatingFinal, ROtherFinal, RPictureFinal,"
                            "RDirectorFinal, RStoryFinal, Usercount, AttitudeCount, TotalBoxOffice,"
                            "TodayBoxOffice, Rank, ShowDays, isRelease) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)" %
                            table_name, data)
            self.data.remove(data)
        self.cx.commit()

    def output_end(self):
        """
        关闭数据库
        :return:
        """
        if len(self.data) > 0:
            self.output_db('MTime')
        self.cx.close()
