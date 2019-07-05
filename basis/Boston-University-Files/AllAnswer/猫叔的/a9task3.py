#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# a9task3.py
# name:
# e-mail:
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from a8task2_lwd import *  # monte carlo simulation
from a9task2_lwd import *  # efficient frontier

# 下面用到的Pandas知识要去查一下官方文档，根据你需要的功能，按文档中的目录索引快速查找
# 网址： http://pandas.pydata.org/pandas-docs/stable/index.html

# 1
def plot_stock_prices(symbols):
    """
    creates a graph of the historical stock prices for several stocks.
    input: symbols is a list of stock symbols.
    """
    df = get_stock_prices_from_csv_files(symbols)
    # 返回了一个 股票收盘价的DataFrame对象

    df = df.loc['2011':'2015',]  # .loc[行条件, 列条件]
    # 查这个.loc 的官方文档网址：在总目录的 Indexing and Selecting Data 条目下面
    # http://pandas.pydata.org/pandas-docs/stable/indexing.html
    # 要学会快速查资料
    # .loc is primarily label based, but may also be used with a boolean array
    # A slice object with labels 'a':'f' (note that contrary to usual python slices,
    # both the start and the stop are included, when present in the index!）

    plt.plot(df)
    plt.title('stock prices')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.legend(symbols)
    #plt.legend(dataframe.columns)  #dataframe.columns --->列标签,做为图例的标签
    # 用这一句也是一样的，实参symbols和dataframe.columns得到的是相同的内容
    plt.show()


# test 1:
symbols = ['AAPL',  'DIS', 'GOOG', 'KO', 'WMT']
plot_stock_prices(symbols)


# 2
def plot_stock_cumulative_change(symbols):
    """
    creates a graph of the cumulative stock returns for several stock.
        (the cumulative change in price since the starting point.)
    input: symbols is a list of stock symbols.
    """

    df = get_stock_prices_from_csv_files(symbols)
    df = df.loc['2011':'2015',]
    df = df / df.iloc[0, :]  # 行条件是 0 表示第一行，列条件是 : 表示所有的列
    # .iloc is primarily integer position based (from 0 to length-1 of the axis),
    # but may also be used with a boolean array.
    # 每行数据除以第1行（行号为0）的数据，就得到了相对于起始行的比率

    plt.plot(df)
    plt.title('stock prices')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.legend(symbols)
    plt.show()

# test 2:
symbols = ['AAPL',  'DIS', 'GOOG', 'KO', 'WMT']
plot_stock_prices(symbols)


# 3
def plot_simulated_stock_returns(s, mu, sigma, t, ntrials):
    """
    create a plot of simulated stock prices.
    input:
        s, the current (initial) stock price
        mu, the mean rate of return on the stock
        sigma, the standard deviation of the rate of return on the stock
        t, the time period for which to run the simulation (in years)
        ntrials, the number of trials to plot on the graph
    """
    o = MCStockOption(s, s, mu, sigma, t, t*12, 1)
    # 这里要去把a8task2.py中的MCStockOption()看一下，理解这个类是如何定义的，其中的方法是干什么的
    for i in range(ntrials):
        prices = o.generate_stock_prices()
        plt.plot(prices)

    plt.xlabel('Periods')
    plt.ylabel('Stock Price')
    plt.title('Simulated Stock Returns')
    plt.show()

# test 3:
plot_simulated_stock_returns(100, 0.10, 0.3, 1, 1)
plot_simulated_stock_returns(100, 0.10, 0.3, 1, 10)
plot_simulated_stock_returns(100, 0.10, 0.3, 20, 10)
# 注意：因为MCStockOption() 里用了random.gauss(0, 1) 模拟，
# 所以，每次执行上面的语句得到的结果都是不同的

# 4
def plot_efficient_frontier(symbols):
    """
    create a graph of the efficient frontier (the set of minimum variance portfolios)
    that can be achieved using a small set of assets.
    """
    # Re-use the functions get_stock_returns_from_csv_files(symbols)
    # and get_covariance_matrix(returns) to obtain the stock symbols
    # and returns, and covariance matrix.
    returns = get_stock_returns_from_csv_files(symbols)
    v = np.matrix(get_covariance_matrix(returns))  # 协方差阵, DataFrame 转换成 np.matrix

    # Calculate the average return for each stock,
    # and create a np.matrix of returns.
    e = np.matrix(returns.mean())

    w = calc_global_min_variance_portfolio(v)
    mid_r = calc_portfolio_return(e, w)

    # Use the function np.linspace(start, stop) to create a set of
    # desired rates of return (rs) at which to find efficient portfolios.
    rs = np.linspace(mid_r - 0.05, mid_r + 0.1)

    # Use your calc_efficient_portfolios_stdev(e, v, rs) function
    # to calculate the standard deviations of the set of efficient portfolios,
    # corresponding to the desired rates of return rs.
    vs = calc_efficient_portfolios_stdev(e, v, rs)

    # Plot the resulting efficient frontier.
    plt.plot(vs,rs)
    plt.xlabel('Standard Deviation')
    plt.ylabel('Expected Return')
    plt.title('Efficient Frontier')
    plt.show()

plot_efficient_frontier(symbols)
