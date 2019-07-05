#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# a9task2.py
# name:
# e-mail:
"""

# 1-4题纯粹是数学知识用编程语言的实现。把相关数学知识对应的公式搞懂就能写出程序了

import numpy as np
import pandas as pd

# 1
def calc_portfolio_return(e, w):
    """
    e is a matrix of expected returns for the assets
    w is a matrix of portfolio weights of the assets, which sums to 1
    returns the portfolio return (as a float) for a portfolio of n >= 2 assets.
    """
    # 网页上的那个w'（w 一撇）表示w.T
    er= e * w.T
    return er[0,0]

## test 1:
#>>> e = np.matrix([0.1, 0.11, 0.08])
#>>> w = np.matrix([1,1,1]) / 3
#>>> calc_portfolio_return(e, w)
#0.09666666666666668
#>>> # another example
#>>> e = np.matrix([0.12, 0.05, 0.09])
#>>> w = np.matrix([0.3, 0.4, 0.3])
#>>> calc_portfolio_return(e, w)
#0.083

# 2
def calc_portfolio_stdev(v, w):
    """
    returns the portfolio standard deviation
        (as a float) for a portfolio of n >= 2 assets.
    input:
        w is a matrix of expected returns for the assets
        v is a matrix of covariances among the assets.
    """
    var = w * v * w.T
    return var[0,0]**0.5


## test 2:
#>>> w = np.matrix([0.4, 0.3, 0.3])
#>>> v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
#>>> calc_portfolio_stdev(v, w)
#0.23345235059857505
#>>> # another example
#>>> w = np.matrix([0.3, 0.5, 0.2])
#>>> v = np.matrix([[0.2, 0.1, 0.5], [0.1, 0.1, 0.2], [0.5, 0.2, 0.3]])
#>>> calc_portfolio_stdev(v, w)
#0.4301162633521313

# 3
def calc_global_min_variance_portfolio(v):
    """
     returns the portfolio weights corresponding to the global minimum variance portfolio.
     input: v is the matrix of covariances among the assets.
    """
    d = len(v)
    vec_of_1 = np.ones((d,1))
    return (v**-1 * vec_of_1 / (vec_of_1.T * v**-1 * vec_of_1)).T

# test 3:
#>>> # first example:
#>>> e = np.matrix([0.1, 0.11, 0.08])
#>>> v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
#>>> w = calc_global_min_variance_portfolio(v)
#>>> w # these are the portfolio weights for the global minimum variance portfolio
#matrix([[ 0.23076923,  0.46153846,  0.30769231]])
#>>> # this is the rate of return on the global minimum variance portfolio
#>>> calc_portfolio_return(e, w)
#0.09846153846153845
#>>> # this is the standard deviation on the global minimum variance portfolio
#>>> calc_portfolio_stdev(v, w)
#0.21483446221182986
#
#>>> # second example
#>>> e = np.matrix([0.12, 0.09, 0.07])
#>>> v = np.matrix([[0.2, 0.1, 0.15], [0.1, 0.1, 0.4], [0.15, 0.4, 0.1]])
#>>> w = calc_global_min_variance_portfolio(v)
#>>> w # these are the portfolio weights for the global minimum variance portfolio
#matrix([[ 0.6122449 ,  0.14285714,  0.24489796]])
#>>> # this is the rate of return on the global minimum variance portfolio
#>>> calc_portfolio_return(e, w)
#0.10346938775510206
#>>> # this is the standard deviation on the global minimum variance portfolio
#>>> calc_portfolio_stdev(v, w)
#0.41649656391752155


# 4
def calc_min_variance_portfolio(e, v, r):
    """
    returns the portfolio weights corresponding to the minimum variance
        portfolio for the required rate of return r.
    input:
        e is a matrix of expected returns for the assets
        v is a matrix of covariances among the assets.
        r is the required rate of return
    """
    d = len(v)
    a = e * v**-1 * e.T
    b = e * v**-1 * np.ones((d,1))
    c = np.ones((1,d)) * v**-1 * np.ones((d,1))
    l1 = (c*r - b)/(a*c - b*b)
    l2 = (a - b*r)/(a*c - b*b)
    return (v**-1 * e.T * l1 +  v**-1 * np.ones((d,1)) * l2).T

## test 4:
#>>> # consider these three assets and the covariance matrix:
#>>> e = np.matrix([0.1, 0.11, 0.08])
#>>> v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
#>>> # find minimum variance portfolio for r = 0.09
#>>> w = calc_min_variance_portfolio(e, v, 0.09)
#>>> w # these are the portfolio weights
#matrix([[ 0.21276596,  0.19148936,  0.59574468]])
#>>> calc_portfolio_return(e, w)
#0.08999999999999958
#>>> calc_portfolio_stdev(v, w)
#0.2568218191830864
#>>>
#>>> # find minimum variance portfolio for r = 0.10
#>>> w = calc_min_variance_portfolio(e, v, 0.10)
#>>> w # these are the portfolio weights
#matrix([[ 0.23404255,  0.5106383 ,  0.25531915]])
#>>> calc_portfolio_return(e, w)
#0.09999999999999953
#>>> calc_portfolio_stdev(v, w)
#0.21635274585338046
#>>>
#>>> # find minimum variance portfolio for r = 0.11
#>>> w = calc_min_variance_portfolio(e, v, 0.11)
#>>> w # these are the portfolio weights
#matrix([[ 0.25531915,  0.82978723, -0.08510638]])
#>>> calc_portfolio_return(e, w)
#0.10999999999999946
#>>> calc_portfolio_stdev(v, w)
#0.28806027738002005


# 5
def calc_efficient_portfolios_stdev(e, v, rs):
    """
    finds a series of minimum variance portfolios and returns their standard deviations.
    input:
        e is a matrix of expected returns for the assets
        v is a matrix of covariances among the assets.
        rs is a numpy.array of rates of return for which to calculate
            the corresponding minimum variance portfolio’s standard deviation
    """
    sigmas = []
    for r in rs.tolist():   #这个.tolist() 作用是 numpy.array 转换成 list
        w = calc_min_variance_portfolio(e, v, r)
        sigma = calc_portfolio_stdev(v, w)
        print('r = %.4f, sigma = %.4f, w = %s' % (r, sigma, w))
        sigmas += [sigma]

    sigmas = np.array(sigmas)

    return sigmas

## test 5:
#>>> e = np.matrix([0.1, 0.11, 0.08])
#>>> v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
#>>> rs = np.linspace(0.07, 0.12, 10) # generate 10 steps between 0.07 and 0.12
#>>> rs # these are the rates of return for which to find efficient portfolios
#array([ 0.07      ,  0.07555556,  0.08111111,  0.08666667,  0.09222222,
#        0.09777778,  0.10333333,  0.10888889,  0.11444444,  0.12      ])
#>>> sigmas = calc_efficient_portfolios_stdev(e, v, rs)
#r = 0.0700, sigma = 0.5198  w = [[ 0.17021277 -0.44680851  1.27659574]]
#r = 0.0756, sigma = 0.4374  w = [[ 0.1820331  -0.26950355  1.08747045]]
#r = 0.0811, sigma = 0.3597  w = [[ 0.19385343 -0.09219858  0.89834515]]
#r = 0.0867, sigma = 0.2909  w = [[ 0.20567376  0.08510638  0.70921986]]
#r = 0.0922, sigma = 0.2386  w = [[ 0.21749409  0.26241135  0.52009456]]
#r = 0.0978, sigma = 0.2151  w = [[ 0.22931442  0.43971631  0.33096927]]
#r = 0.1033, sigma = 0.2296  w = [[ 0.24113475  0.61702128  0.14184397]]
#r = 0.1089, sigma = 0.2761  w = [[ 0.25295508  0.79432624 -0.04728132]]
#r = 0.1144, sigma = 0.3418  w = [[ 0.26477541  0.97163121 -0.23640662]]
#r = 0.1200, sigma = 0.4177  w = [[ 0.27659574  1.14893617 -0.42553191]]
#>>> sigmas # the portfolio standard deviations corresponding to the rates of return rs
#array([ 0.51981994,  0.4373548 ,  0.3597492 ,  0.29091849,  0.23858219,
#        0.21513522,  0.22960548,  0.27609419,  0.34177644,  0.41769377])


# 下面用到的Pandas知识要去查一下官方文档，根据你需要的功能，按文档中的目录索引快速查找
# 官方网址： http://pandas.pydata.org/pandas-docs/stable/index.html
# 6
def get_stock_prices_from_csv_files(symbols):
    """
    input: symbols is a list of stock symbols
    return value will be a pandas.DataFrame
        containing the monthly stock prices for each of those stock symbols,
        for the period of dates given in the CSV files.
    """
    # 参数symbols是一个列表，里面存放的是stock的名字。
    # symbols = ['AAPL', 'DIS', 'GOOG', 'HSY', 'KO', 'WMT']

    # 注意：下面datas 变量里的文件夹路径要修改成你自己电脑里的实际使用的文件夹的路径
    # 例如，我把网页上的那几个.csv文件下载并保存在了 E:\PythonTask\a9\ 文件夹下面
    # 那么，就要修改为：datas = ('E:/PythonTask/a9/'+ s + '-monthly.csv' for s in symbols)
    # 首先把下面的语句复制到交互模式做个测试：
    # >>> symbols = ['AAPL', 'DIS', 'GOOG', 'HSY', 'KO', 'WMT']
    # >>> datas = ('E:/PythonTask/a9/'+ s + '-monthly.csv' for s in symbols)
    # >>> list(datas)  # 看看这3句话执行的结果就明白了

    #datas = ('/Users/tony/Desktop/assg9/'+ s + '-monthly.csv' for s in symbols)
    datas = ['E:/PythonTask/a9/' + s + '-monthly.csv' for s in symbols]  # 列表推导式
    # 这句话的作用就是构造一个symbols中所有stock对应的文件的全名（文件夹路径+文件名）的列表
    # 因为每个stock数据文件的名字命名规则都是一样的，即：stock名+'-monthly.csv'

    adjclose = pd.DataFrame()
    # 创建一个数据框 DataFrame 。类似于 s = set() 创建一个空的集合
    # DataFrame 是一种二维的数据结构，叫数据框。
    # pandas 定义了两个最基本的数据结构：Series 和DataFrame 。（看一下《Pandas的使用.docx》）
    # 一定要搞懂这两种数据结构才能继续往下写程序，不然会不知道为什么

    for data in datas:
        print(data)
        df = pd.read_csv(data)  #读取.csv文件的内容

        df.Date = pd.to_datetime(df.Date, format = '%m/%d/%y')
        # pd.to_datetime() 函数的作用是：Convert argument to datetime.
        # 上面的语句作用是把参数df.Date【就是.csv文件中的Date列】转换成format指定的格式的日期时间类型

        adjclose = pd.concat([adjclose, df.set_index('Date')['Adj Close']], axis= 1)
        # pd.concat()函数是将数据融合在一起。
        # for循环每次读出一个.csv文件的内容，现在，把所有文件的数据融合到一个pd.DataFrame里
        # axis = 1 ,表示按行来合并。如果axis = 0 则按列来合并
        # df.set_index('Date')['Adj Close'] 意思是按'Date'列索引（可理解成排序），
        # 并且只取每个stock数据的'Adj Close'列的数据（其他列的数据不需要了）
        # 最后得到的DateFrame里包含的就是全部股票的'Adj Close'(收盘价)列的数据清单
        # 下面的网址讲解了concat()方法：
        # 官方网址是这个：http://pandas.pydata.org/pandas-docs/stable/merging.html
        # 有个中文网址是：http://www.cnblogs.com/liuq/p/7019262.html

    adjclose.columns = symbols
    # 把列名称设置成参数symbols列表中的名称

    return adjclose
    # 最后，返回我们构造好的包含了各个股票收盘价的DataFrame

## test 6:
#symbols = ['AAPL', 'DIS', 'GOOG', 'HSY', 'KO', 'WMT']
#adjclose = get_stock_prices_from_csv_files(symbols)
#print(adjclose)
##Remeber you can use pandas.DataFrame.head() to view the first 5 rows of the data frame.
#pd.DataFrame.head(adjclose)


# 7
def get_stock_returns_from_csv_files(symbols):
    """
    return a single pandas.DataFrame object containing the stock returns
    """
    # 本题的要求就是：返回股票的收益。即每天股票的收盘价比上一日涨/跌了多少(百分比)
    # 即：（某天的收盘价 - 上一天的收盘价）/ 上一天的收盘价

    adjclose = get_stock_prices_from_csv_files(symbols)

    rets = adjclose.pct_change()
    # pct_change()：Series也有这个函数，这个函数用来计算同colnums两个相邻的数字之间的变化率。

    return rets

# test 7:
#>>> symbols = ['AAPL',  'DIS', 'GOOG', 'KO', 'WMT']
#>>> # note that the function also produces this small printout for debugging
#>>> returns = get_stock_returns_from_csv_files(symbols)
#
#>>> returns.head()
##                AAPL       DIS      GOOG        KO       WMT
##2007-11-01       NaN       NaN       NaN       NaN       NaN
##2007-12-01  0.087037 -0.026244 -0.002193 -0.006391 -0.007724
##2008-01-01 -0.316640 -0.065603 -0.183924 -0.038618  0.072348
##2008-02-01 -0.076389  0.086126 -0.165019 -0.009153 -0.022664
##2008-03-01  0.147817 -0.031780 -0.065177  0.041225  0.062311


# 8
def get_covariance_matrix(returns):
    """
    input: The parameter return will be a pandas.DataFrame object
    return: generates a covariance matrix for the stock returns in returns.
    """
    return returns.cov()  # 协方差阵(returns is a DataFrame)


## test 8
#>>> symbols = ['AAPL',  'DIS', 'GOOG', 'KO', 'WMT']
#>>> # note that the function also produces this small printout for debugging
#>>> returns = get_stock_returns_from_csv_files(symbols)
#
#>>> covar = get_covariance_matrix(returns)
#>>> covar
##          AAPL       DIS      GOOG        KO       WMT
##AAPL  0.007775  0.002384  0.003823  0.001165  0.000468
##DIS   0.002384  0.004245  0.002378  0.001221  0.000410
##GOOG  0.003823  0.002378  0.006470  0.000995  0.000348
##KO    0.001165  0.001221  0.000995  0.001941  0.000726
##WMT   0.000468  0.000410  0.000348  0.000726  0.002221