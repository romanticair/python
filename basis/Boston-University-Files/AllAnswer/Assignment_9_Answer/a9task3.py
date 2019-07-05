import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from a8task2 import  *  # monte carlo simulation
from a9task2 import  *  # efficient frontier

"""
# a9task1.py
# name:
# e-mail:

"""

def plot_stock_prices(symbols):
    """
    symbols is a list of stock.
    creates a graph of the historical stock prices for several stocks.

    """
    prices = get_stock_prices_from_csv_files(symbols)
    months = mdates.MonthLocator()
    years = mdates.YearLocator()
    datesFmt = mdates.DateFormatter('%Y') # -%m-%d
    dates = [dt.date(2011 + i, 1, 1) for i in range(5)]
    fig ,ax = plt.subplots()

    plt.plot(dates, prices)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(datesFmt)
    ax.xaxis.set_minor_locator(months)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title("Stock prices")
    plt.legend(['AAPL', 'GOOG', 'KO', 'VTMSX'], loc = 2)
    plt.show()

def plot_stock_cumulative_change(symbols):
    """
    This function should take a parameter which is a list
    of stock symbols. For each stock symbol, the function
    will expect a .csv file containing stock price data
    (i.e., from Yahoo Finance), with monthly stock prices

    """
    import pandas as pd

    prices = get_stock_prices_from_csv_files(symbols)
    row = len(prices)
    cumulativeChange = pd.DataFrame(np.arange(prices.size).reshape((row, prices.size // row)))
    cumulativeChange.index = prices.index.copy()
    cumulativeChange.columns = prices.columns.copy()

    cumulativeChange.ix[0] = 1.0  # 行索引

    for stock in prices.columns:
        for i in range(1, row):
            cumulativeChange[stock][i] = prices[stock][i] - prices[stock][i - 1]

    months = mdates.MonthLocator()
    years = mdates.YearLocator()
    datesFmt = mdates.DateFormatter('%Y')  # -%m-%d
    dates = [dt.date(2011 + i, 1, 1) for i in range(5)]
    fig, ax = plt.subplots()

    plt.plot(dates, cumulativeChange)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(datesFmt)
    ax.xaxis.set_minor_locator(months)

    plt.xlabel('Date')
    plt.ylabel('Relative Price')
    plt.title("Cumulative change in stock prices")
    plt.legend(['AAPL', 'GOOG', 'KO', 'VTMSX'], loc = 2)
    plt.show()

def plot_simulated_stock_returns(s, mu, sigma, t, ntrials):
    """
    s, the current (initial) stock price
    mu, the mean rate of return on the stock
    sigma, the standard deviation of the rate of return on the stock
    t, the time period for which to run the simulation (in years)
    ntrials, the number of trials to plot on the graph

    """
    # use MCStockOption as stock price generator
    o = MCStockOption(s, s, mu, sigma, t, t * 12, 1)
    # create ntrials runs of stock prices
    for i in range(ntrials):
        prices = o.generate_stock_prices()
        plt.plot(prices)

    plt.title("Simulated Stock Returns")
    plt.xlabel("Periods")
    plt.ylabel("Stock Price")
    plt.show()

def plot_efficient_frontier(symbols):
    """
    create a graph of the efficient frontier
    (the set of minimum variance portfolios) that can
    be achieved using a small set of assets.

    """
    # 收益
    stocksReturn = get_stock_returns_from_csv_files(symbols)
    # 协方差矩阵
    v = np.matrix(get_covariance_matrix(stocksReturn))
    # 平均回报
    temp = stocksReturn.mean()
    e = np.matrix(temp)
    # 创建一组期望收益率Rs
    globalMinVariance = calc_global_min_variance_portfolio(v) # 全局最小方差组合
    r = 0.12 # My desired rates of return
    minVariance = calc_min_variance_portfolio(e, v, r)
    returns1 = calc_portfolio_return(e, globalMinVariance) # 投资收益1
    returns2 = calc_portfolio_return(e, minVariance) # 投资收益2
    rs = np.linspace(returns1, returns2) # A set of desired rates of return to find efficient portfolios
    # 计算有效投资组合集合的标准偏差, 对应于期望的收益率rs
    stdev = calc_efficient_portfolios_stdev(e, v, rs)
    # 边界图
    plt.plot(stdev, rs)
    plt.show()

def test_4():
    symbols = ['AAPL', 'GOOD', 'KO', 'VTMSX']
    plot_efficient_frontier(symbols)

test_4()

def test_1():
    symbols = ['AAPL', 'GOOD', 'KO', 'VTMSX']
    plot_stock_prices(symbols)

# test_1()
def test_2():
    symbols = ['AAPL', 'GOOD', 'KO', 'VTMSX']
    plot_stock_cumulative_change(symbols)

# test_2()

def test_3():
    # This is a plot of a single simulated price path (trial)
    # for 1 year (12 periods/year).
    plot_simulated_stock_returns(100, 0.10, 0.3, 1, 1)
    # This is a plot of 10 simulated price paths (trials)
    # for 1 year (12 periods/year).
    plot_simulated_stock_returns(100, 0.10, 0.3, 1, 10)
    # This is a plot of 10 simulated price paths (trials)
    # for 20 years (12 periods/year).
    plot_simulated_stock_returns(100, 0.10, 0.3, 20, 10)

# test_3()