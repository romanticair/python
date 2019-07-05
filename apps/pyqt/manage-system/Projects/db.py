import time
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlQuery, QSqlDatabase, QSqlTableModel, QSqlRelationalTableModel,
                         QSqlRelation)

ORDER = None
ID = 0
NAME = 1
GENDER = 2
DEPARTMENT = 3

createyear = time.strftime("%y")
createmoth = time.strftime("%m")


def open_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("management{0}.db".format(createyear))
    db.setUserName("root")
    db.setPassword("root")
    return db


def init_tables():
    print("Create tabls")
    dptQuery = QSqlQuery()
    clkQuery = QSqlQuery()

    # 部门表
    dptQuery.exec("""CREATE TABLE departments{0}(
                dpt_id VARCHAR(5) PRIMARY KEY UNIQUE NOT NULL,
                dpt_name VARCHAR(20))
                """.format(createmoth))

    # 员工表
    # clk_gender ENUM('Female', 'Male'),
    # AUTOINCREMENT 错在哪里了呢？
    clkQuery.exec("""CREATE TABLE clerks{0}(
                clk_id VARCHAR(5) PRIMARY KEY UNIQUE NOT NULL,
                clk_name VARCHAR(20) NOT NULL,
                clk_gender VARCHAR(10),
                dpt_id VARCHAR(5),
                CONSTRAINT FK_dpt FOREIGN KEY(dpt_id) REFERENCES departments{1}(dpt_id))
                """.format(createmoth, createmoth))

    """
    # 工资明细表
    query.exec(""CREATE TABLE Detail{0}(
                clk_id VARCHAR(4),
                CONSTRAINT FK_clk FOREIGN KEY(clk_id) REFERENCES Clerk{1}(clk_id))
                "".format(createmoth, createmoth))

    # 工资总表
    query.exec(""CREATE TABLE AllWages{0}(
                allwages_id VARCHAR(4) PRIMARY KEY UNIQUE,
                maker_id VARCHAR(4),
                examiner_id VARCHAR(4) DEFAULT @maker_id,
                approver_id VARCHAR(4) DEFAULT @maker_id,
                issue_date DATE UNIQUE,
                archiving_status BOOL NOT NULL,
                WS_name VARCHAR(20) UNIQUE NOT NULL,
                CONSTRAINT (FK_clk, FK_clk, FK_clk) FOREIGN KEY(maker_id, examiner_id, approver_id)
                REFERENCES Clerk{1}(clk_id, clk_id, clk_id))
                "".format(createmoth, createmoth))

    # 工资项目及类别表
    query.exec("" CREATE TABLE WageSources{0}(
                 pj_id VARCHAR(4) PRIMARY KEY UNIQUE,
                 pj_name VARCHAR(20) NOT NULL UNIQUE,
                 cls_id VARCHAR(2) NOT NULL,
                 cls_name VARCHAR(20) NOT NULL,
                 show_order INT AUTOINCREMENT
                 )AUTOINCREMENT=1
                 "".format(createmoth))
    ########################################################
    """
    # QApplication.processEvents()

    print("Populating tables ....")
    ########################################################
    # 初始化数据
    dptQuery.exec("INSERT INTO departments{0}(dpt_id, dpt_name)"
                  "VALUES ('D01', '人力资源部')".format(createmoth))
    dptQuery.exec("INSERT INTO departments{0}(dpt_id, dpt_name)"
                  "VALUES ('D02', '销售部')".format(createmoth))
    dptQuery.exec("INSERT INTO departments{0}(dpt_id, dpt_name)"
                  "VALUES ('D03', '宣传部')".format(createmoth))
    dptQuery.exec("INSERT INTO departments{0}(dpt_id, dpt_name)"
                  "VALUES ('D04', '财务部')".format(createmoth))
    dptQuery.exec("INSERT INTO departments{0}(dpt_id, dpt_name)"
                  "VALUES ('D05', '技术部')".format(createmoth))
    # QApplication.processEvents()

    clkQuery.exec("INSERT INTO clerks{0}(clk_id, clk_name, clk_gender, dpt_id)"
                  "VALUES ('C001', '徐明浩', 'Male', 'D01')".format(createmoth))
    clkQuery.exec("INSERT INTO clerks{0}(clk_id, clk_name, clk_gender, dpt_id)"
                  "VALUES ('C002', '里布奥', 'Male', 'D02')".format(createmoth))
    clkQuery.exec("INSERT INTO clerks{0}(clk_id, clk_name, clk_gender, dpt_id)"
                  "VALUES ('C003', '郄丽思', 'Male', 'D03')".format(createmoth))
    clkQuery.exec("INSERT INTO clerks{0}(clk_id, clk_name, clk_gender, dpt_id)"
                  "VALUES ('C004', '李艳艳', 'Female', 'D04')".format(createmoth))
    clkQuery.exec("INSERT INTO clerks{0}(clk_id, clk_name, clk_gender, dpt_id)"
                  "VALUES ('C005', '陈华华', 'Female', 'D05')".format(createmoth))
    # QApplication.processEvents()
    ########################################################

    # 使用prepare和bindValue组合增加数据
    # 或者query.prepare("INSERT INTO person (id, forename, surname) "VALUES (?, ?, ?)")
    clkQuery.prepare("INSERT INTO clerks{0} (clk_id, clk_name, clk_gender, dpt_id)"
                     "VALUES(:clk_id, :clk_name, :clk_gender, :dpt_id)".format(createmoth))

    id = 6                                                        # 从第六位员工再开始
    names = {'小李': 'Male', '小张': 'Male', '校花': 'Female', '模特': 'Female', '警察': 'Male',
             '服务员': 'Male', '厨师': 'Female', '护士': 'Female', '医生': 'Female', '理发师': 'Male',
             '飞行员': 'Male', '土匪': 'Male', '叛徒': 'Male', '特工': 'Male', '丞相': 'Male',
             '路人丙': 'Male', '路人乙': 'Male', '路人甲': 'Male', '陆军': 'Male', '海军': 'Female'}
    dpts = ['D01', 'D02', 'D03', 'D04', 'D05']
    for i in range(20):
        name = random.choice(list(names))                         # 或者直接迭代
        gender = names[name]                                      # 下述也相同
        clkQuery.bindValue(":clk_id", "C{0:0>3}".format(id + i))   # bindValue(0, id + i)
        clkQuery.bindValue(":clk_name", name)                     # bindValue(1, id + i)
        clkQuery.bindValue(":clk_gender", gender)
        clkQuery.bindValue(":dpt_id", random.choice(dpts))
        clkQuery.exec_()
        # clkQuery.exec("commit")                                 # 不用"commit"也可以
        names.pop(name)                                           # 直接迭代则不用pop
    # QApplication.processEvents()                                # 额外的协助(提高性能)


def model(self):
    model = QSqlRelationalTableModel(self)
    model.setTable('clerks{0}'.format(createmoth))
    model.setEditStrategy(QSqlTableModel.OnManualSubmit)          # 需要手动修改提交数据而不是直接编辑
    model.setRelation(DEPARTMENT, QSqlRelation("departments{0}".format(createmoth), "dpt_id", "dpt_name"))
    model.setSort(ID, Qt.AscendingOrder)
    #  self.model.setHeaderData(0,Qt.Horizontal,QVariant("something"))
    # self.model.setHeaderData(ORDER, Qt.Horizontal, "序号")
    model.setHeaderData(ID, Qt.Horizontal, "编号")
    model.setHeaderData(NAME, Qt.Horizontal, "姓名")
    model.setHeaderData(GENDER, Qt.Horizontal, "性别")
    model.setHeaderData(DEPARTMENT, Qt.Horizontal, "部门")
    model.select()
    return model
