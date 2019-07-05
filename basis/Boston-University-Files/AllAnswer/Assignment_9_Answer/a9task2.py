import numpy as np

"""
# a9task2.py
# name:
# e-mail:

"""

# 1
def calc_portfolio_return(e, w):
    """
    e is a matrix of expected returns for the assets,
    w is a matrix of portfolio weights of the assets,
    which sums to 1.

    Returns the portfolio for a portfolio
    of n >= 2 assets

    """
    return (e * w.T)[0, 0]

# 2
def calc_portfolio_stdev(v, w):
    """
    e is a matrix of expected returns for the assets,
    v is a matrix of covariances among the assets.

    Returns the portfolio standard deviation
    for a portfolio of n >= 2 assets.

    """
    return np.sqrt((w * v * w.T)[0, 0])

# 3
def calc_global_min_variance_portfolio(v):
    """
    find the portfolio with the absolute minimum variance that
    can be composed of the selected assets.

    Returns the portfolio weights corresponding to the
    global minimum variance portfolio

    """
    n = len(v)
    C = np.ones((n, 1)).T * v.I * np.ones((n, 1))
    Wmvp = 1 / C * np.ones((n, 1)).T * v.I

    return Wmvp

# 4
def calc_min_variance_portfolio(e, v, r):
    """
    e is a matrix of expected returns for the assets,
    v is a matrix of covariances among the assets,
    r is the required rate of return.

    Returns the portfolio weights corresponding
    to the minimum variance portfolio for
    the required rate of return r.

    """
    n = e.size
    a = np.ones((1, n)) * v.I * np.matrix(e).T
    b = e * v.I * e.T
    c = np.ones((1, n)) * v.I * np.ones((n, 1))

    A = np.matrix([[b[0, 0], a[0, 0]], [a[0, 0], c[0, 0]]])
    # np.row_stack ? np.column_stack ?
    # np.concatenate() ?        np.vstack() np.hstack()

    d = np.linalg.det(A)

    g = 1 / d * (b * np.ones((1, n)) - a * e) * v.I
    h = 1 / d * (c * e - a * np.ones((1, n))) * v.I
    w = g + h * r

    return w

# 5
def calc_efficient_portfolios_stdev(e, v, rs):
    """
    e is a matrix of expected returns for the assets
    v is a matrix of covariances among the assets.
    rs is a numpy.array of rates of return for which to calculate the
    corresponding minimum variance portfolio’s standard deviation.

    finds a series of minimum variance portfolios and
    returns their standard deviations.

    """
    i = 0
    sigma = np.zeros(rs.size)

    for r in np.nditer(rs):
        w = calc_min_variance_portfolio(e, v, float(r))
        sigma[i] = calc_portfolio_stdev(v, w)
        print("r = {0:<10.4f} sigma = {1:<10.4f} w = {2:}".format(r, sigma[i], w))
        i += 1

    return sigma

# 6
def get_stock_prices_from_csv_files(symbols):  # some troules
    """
    symbols will be a list of stock symbols.

    Return value will be a pandas.DataFrame containing the monthly
    stock prices for each of those stock symbols, for the
    period of dates given in the CSV files.

    """
    import pandas as pd
    from pandas import DataFrame

    dataset = DataFrame()
    datas = DataFrame()

    for name in symbols:
        filedata = pd.read_csv(r"L:\AllPyProgr\WeeklyHomeworks\Assignment 3 — MF 703, Boston University_files\\" + name + '.csv')
        datas[name] = filedata['Adj Close']

    datas['Date'] = filedata['Date']
    dataset['Date'] = filedata['Date']
    # for name in symbols:
    dataset = pd.DataFrame.merge(dataset, datas, on = ['Date'], how = 'outer')
    dataset.index = dataset['Date']
    del dataset['Date']

    # join(self, other, on=None, how='left', lsuffix='', rsuffix='', sort=False)
    return dataset

# 7
def get_stock_returns_from_csv_files(symbols):
    """
    Return a single pandas.DataFrame object
    containing the stock returns.

    """
    import pandas as pd

    returns = get_stock_prices_from_csv_files(symbols)
    n = len(returns)
    results  = pd.DataFrame(np.ones((n, returns.size // n)), index = returns.index, columns = symbols)

    for name in symbols:
        for i in range(0, n):
            results[name][i] = (returns[name][i] - returns[name][i - 1]) / returns[name][i]

    results[0:1] = np.nan
    results.index.name = None
    return results

# 8
def get_covariance_matrix(returns):
    """
    generates a covariance matrix for the stock returns
    in returns.

    Return a pandas.DataFrame object (dimensions n * n)

    """
    import pandas as pd
    import a3_task1

    n = len(returns)
    covar = returns.drop('2012/1/10')

    # Every stocks' returns lists
    returnslst = [covar[stockcode].copy() for stockcode in covar.columns]
    returnsseries = pd.Series(returnslst, index = covar.columns)
    covar.index = [covar.columns]

    # covar = pd.DataFrame(np.random.random((n - 1, n - 1)), index = returns.columns, columns = returns.columns)
    # for name in returns.columns:
    #     covar[name]

    for stocki in covar.columns:
        for stockc in covar.columns:
            funcvalue = a3_task1.covariance(list(returnsseries[stocki]), list(returnsseries[stockc]))
            covar[stocki][stockc] = funcvalue

    return covar


# Test :
def test_8():
    symbols = ['AAPL', 'GOOD', 'KO', 'VTMSX']
    returns = get_stock_returns_from_csv_files(symbols)
    covar = get_covariance_matrix(returns)
    print(covar)

    """
              AAPL       DIS      GOOD        KO       WMT
    AAPL  0.007775  0.002384  0.003823  0.001165  0.000468
    DIS   0.002384  0.004245  0.002378  0.001221  0.000410
    GOOG  0.003823  0.002378  0.006470  0.000995  0.000348
    KO    0.001165  0.001221  0.000995  0.001941  0.000726
    WMT   0.000468  0.000410  0.000348  0.000726  0.002221

    """

# test_8()

def test_7():
    symbols = ['AAPL', 'GOOD', 'KO', 'VTMSX']
    returns = get_stock_returns_from_csv_files(symbols)
    print(returns)
    """
                    AAPL      GOOD        KO     VTMSX
    Date
    2012/1/10       NaN       NaN       NaN       NaN
    2012/1/11 -0.021641  0.014865  0.002042  0.012780
    2012/1/12  0.016633 -0.019101  0.002761 -0.016379
    2012/1/13  0.015339  0.013074 -0.013031  0.011232
    2012/1/17  0.004378 -0.006133  0.011514 -0.005264

    """
# test_7()

def test_6():
    symbols = ['AAPL', 'GOOD', 'KO', 'VTMSX']
    datas = get_stock_prices_from_csv_files(symbols)
    print(datas)

    # For example
    """
    File: AAPL-monthly.csv

    Date,Open,High,Low,Close,Adj Close,Volume
    11/1/07,26.942858,27.525715,21.518572,26.031429,23.419334,6549947600
    12/1/07,25.98,28.994286,25.284286,28.297142,25.457693,4313169700
    1/1/08,28.467142,28.608572,18.02,19.337143,17.396778,8793472100
    2/1/08,19.462856,19.512857,16.491428,17.860001,16.067854,6216488600
    3/1/08,17.777143,20.82,16.857143,20.5,18.442949,5731818400
    4/1/08,20.9,25.714285,20.515715,24.85,22.356453,5696745600
    5/1/08,24.994286,27.462856,24.571428,26.964285,24.258581,4647053600

    """
# test_6()




def test_5():
    e = np.matrix([0.1, 0.11, 0.08])
    v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
    rs = np.linspace(0.07, 0.12, 10)  # generate 10 steps between 0.07 and 0.12
    print(rs)  # these are the rates of return for which to find efficient portfolios
    # array([0.07, 0.07555556, 0.08111111, 0.08666667, 0.09222222,
    #        0.09777778, 0.10333333, 0.10888889, 0.11444444, 0.12])

    sigmas = calc_efficient_portfolios_stdev(e, v, rs)
    # r = 0.0700, sigma = 0.5198  w = [[0.17021277 - 0.44680851  1.27659574]]
    # r = 0.0756, sigma = 0.4374  w = [[0.1820331 - 0.26950355  1.08747045]]
    # r = 0.0811, sigma = 0.3597  w = [[0.19385343 - 0.09219858  0.89834515]]
    # r = 0.0867, sigma = 0.2909  w = [[0.20567376  0.08510638  0.70921986]]
    # r = 0.0922, sigma = 0.2386  w = [[0.21749409  0.26241135  0.52009456]]
    # r = 0.0978, sigma = 0.2151  w = [[0.22931442  0.43971631  0.33096927]]
    # r = 0.1033, sigma = 0.2296  w = [[0.24113475  0.61702128  0.14184397]]
    # r = 0.1089, sigma = 0.2761  w = [[0.25295508  0.79432624 - 0.04728132]]
    # r = 0.1144, sigma = 0.3418  w = [[0.26477541  0.97163121 - 0.23640662]]
    # r = 0.1200, sigma = 0.4177  w = [[0.27659574  1.14893617 - 0.42553191]]

    print(sigmas) # the portfolio standard deviations corresponding to the rates of return rs
    # array([0.51981994, 0.4373548, 0.3597492, 0.29091849, 0.23858219,
    #        0.21513522, 0.22960548, 0.27609419, 0.34177644, 0.41769377])



def test_4():
    # consider these three assets and the covariance matrix:
    e = np.matrix([0.1, 0.11, 0.08])
    v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])

    # find minimum variance portfolio for r = 0.09
    w = calc_min_variance_portfolio(e, v, 0.09)
    print(w)  # these are the portfolio weights
    # [[0.21276596, 0.19148936, 0.59574468]]

    print(calc_portfolio_return(e, w))
    # 0.08999999999999958

    print(calc_portfolio_stdev(v, w))
    # 0.2568218191830864


def test_3():
    # first example:
    e = np.matrix([0.1, 0.11, 0.08])
    v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
    w = calc_global_min_variance_portfolio(v)
    print(w)
    # these are the portfolio weights for the global minimum variance portfolio
    # [[0.23076923, 0.46153846, 0.30769231]]

    # this is the rate of return on the global minimum variance portfolio
    print(calc_portfolio_return(e, w))
    # 0.09846153846153845

    # this is the standard deviation on the global minimum variance portfolio
    print(calc_portfolio_stdev(v, w))
    # 0.21483446221182986

    # second example:
    e = np.matrix([0.12, 0.09, 0.07])
    v = np.matrix([[0.2, 0.1, 0.15], [0.1, 0.1, 0.4], [0.15, 0.4, 0.1]])
    w = calc_global_min_variance_portfolio(v)
    # these are the portfolio weights for the global minimum variance portfolio
    print(w)
    # [[0.6122449, 0.14285714, 0.24489796]]

    # this is the rate of return on the global minimum variance portfolio
    print(calc_portfolio_return(e, w))
    # 0.10346938775510206

    # this is the standard deviation on the global minimum variance portfolio
    print(calc_portfolio_stdev(v, w))
    # 0.41649656391752155


def test_2():
    w = np.matrix([0.4, 0.3, 0.3])
    v = np.matrix([[0.2, 0, 0], [0, 0.1, 0], [0, 0, 0.15]])
    print(calc_portfolio_stdev(v, w))
    # 0.23345235059857505

    # another example
    w = np.matrix([0.3, 0.5, 0.2])
    v = np.matrix([[0.2, 0.1, 0.5], [0.1, 0.1, 0.2], [0.5, 0.2, 0.3]])
    print(calc_portfolio_stdev(v, w))
    # 0.4301162633521313


def test_1():
    e = np.matrix([0.1, 0.11, 0.08])
    w = np.matrix([1, 1, 1]) / 3
    print(calc_portfolio_return(e, w))
    # 0.09666666666666668

    # another example
    e = np.matrix([0.12, 0.05, 0.09])
    w = np.matrix([0.3, 0.4, 0.3])
    print(calc_portfolio_return(e, w))
    # 0.083

