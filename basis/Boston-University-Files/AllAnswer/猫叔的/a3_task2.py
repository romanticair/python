"""
a3_task2.py --- Assignment 3 Task 2

Name: 
Email: 
"""

# 1.
def calc_returns(prices):
    """
    input: a list of stock prices 
    return: a list of the periodic returns
    """

    ri = []
    n = 0
    for i in prices:
        if n < len(prices) - 1:  # 注意：列表中元素编号是从0开始的，len(prices)返回的是元素的个数
            n += 1
            rn = prices[n] / i - 1
            ri.append(rn)
    return ri


prices = [100, 110, 105, 112, 115]
returns = calc_returns(prices)
print(returns)


# 2.
def process_stock_prices_csv(filename):
    """
    input:  a data file containing stock price data
    return: a list of stock prices
    
    # 关于参数filename的要求：
    # 
    # filname指向的文件中包含的内容是用逗号分隔开的数据项（.csv格式文件）
    # 第一行是表头（列描述），本函数会忽略掉该行；
    # 第二行开始为数据行，每行数据的倒数第2项的数据是股票收盘价格
    """

    mydata = []  # Create an empty list to hold the prices

    f = open(filename)

    for line in f.readlines()[1:]:  # Read and discard the first line
        mydata.append(float(line.split(',')[-2]))
        # split using comma as separator
        # Convert this price into a floating-point number (float), and append it to the list

    f.close()

    return mydata


# Note that the filename will depend on where you save the file on your computer.
# This filename works for my computer only!

filename = 'E:/PythonTask/a3/AAPL.csv'
prices = process_stock_prices_csv(filename)

# 3.

from a3_task1 import *

def stock_report(filenames, vtsmx_filename):
    """
    filenames: a list containing some data files that containing stock price data
    vstsmx_filename: a data file containing  the stock market index (VTSMX)
    return : This program will process several CSV files to obtain stock prices 
              (for the same time periods) for 5 different stocks, 
              and produce several outputs. 
        
    #参数说明：
    #filenames: 是个列表，包含5个列表项（是文件名称），其对应文件中包含了股票价格数据，
    #           其格式和文件“E:/PythonTask/AAPL.csv”相同（用逗号分隔的数据）
    #          （参见上面那个函数 process_stock_prices_csv(filename)的说明）
    #vstsmx_filename:是包含股票指数数据的文件（从 Yahoo Finance 网站获取的数据）。
    #格式要求：filenames中的每个文件的记录
    """

    # 将VTSMX数据处理成一个列表
    vtsmx = process_stock_prices_csv(vtsmx_filename)  # 需要从Yahoo下载数据，格式整理成和股票数据文件相同

    ret_list = []  # 用于存放处理好的数据
    for filename in filenames:
        # step 0: 取股票名称
        # 文件名就是股票名（例：aapl.scv --- 截取得到“aapl”即是）
        stock_name = filename.split("/")[-1][:-4]  # “aapl.scv,[:-4]得到句点（.）前面的就是股票名称

        # step 1: read the stock price data from the file,
        # and obtain a list containing only the stock prices (no other fields)
        # 从文件中读取股票价格数据
        prices = process_stock_prices_csv(filename)

        # step 2: Calculate the stock returns
        # 获得收益的列表
        returns = calc_returns(prices)

        # step 3: Find the mean and standard deviation of returns
        # 计算回报的平均值和标准偏差

        means = mean(returns)  # 均值
        stdevs = stdev(prices)  # 标准差

        # compare each stock to the stock market index (VTSMX)
        covar = covariance(prices, vtsmx)  # 总体协方差
        correl = correlation(prices, vtsmx)  # 相关系数
        r_sq = rsq(prices, vtsmx)  # the square of the correlation
        beta = simple_regression(prices, vtsmx)[1]
        alpha = simple_regression(prices, vtsmx)[0]

        # step 4: append to result list
        ret_list.append([stock_name, means, stdevs, covar, correl, r_sq, beta, alpha])

    # step 5: print them out in a nicely formatted table
    print("Descriptive statistics for annual stock returns:")
    print("Symbol      Mean      StDev     Covar     Correl    R-SQ      Beta      Alpha")

    for data in ret_list:
        # 构造输出格式字符串
        line = "{0:8}{1:10.4f}{2:10.4f}{3:10.4f}{4:10.4f}{5:10.4f}{6:10.4f}{7:10.4f}".format(data[0], data[1], data[2],
                                                                                             data[3], data[4], data[5],
                                                                                             data[6], data[7])
        print(line)

# test of def stock_report(filenames, vtsmx_filename):

stock_file = ["E:/PythonTask/a3/AAPL.CSV", "E:/PythonTask/a3/GOOD.CSV", "E:/PythonTask/a3/KO.CSV"]
vtmsx_file = "E:/PythonTask/a3/VTMSX.CSV"
stock_report(stock_file, vtmsx_file)
