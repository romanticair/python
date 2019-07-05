import numpy as np

"""
# a9task1.py
# name:
# e-mail:

"""


def bond_price(times, cashflows, rate):
    """
    times is a list of the times at which the cashflows occur;
    cashflows is a list of the cashflows for this bond;
    r is the periodic (not annual) discount rate.

    Returns the price of a bond

    """
    d = 1 / (1 + rate) ** np.asarray(times)
    cf = np.matrix(cashflows)
    p = d * cf.T

    return p[0, 0]

def bond_duration(times, cashflows, rate):
    """
    times is a list of the times at which the cashflows occur;
    cashflows is a list of the cashflows for this bond;
    r is the periodic (not annual) discount rate.

    Return the duration metric for a bond.

    """
    b = bond_price(times, cashflows, rate)   # Price of the bond
    t = np.array(times) # np.array of the times
    c = np.array(cashflows) # np.array of the bonds' cashflows
    d = np.matrix(1 / (1 + rate) ** t) # np.matrix of discount factors
    # ???

    duration = 1 / b * t * c * d.T
    return duration[0, 0]

def bootstrap(cashflows, prices):
    """
    cashflows is a matrix(2-dimensional list) containing the cashflows for
    some bonds, and prices is a column matrix(2-dimensional list)
    containing the prices of these bonds.

    """
    # zero-coupon bonds

    p = np.matrix(prices) # a matrix containing the price of the bond
    cf = np.matrix(cashflows) # the matrix of the bonds' cashflows
    d = cf.I * p.T # the matrix of implied discount factors
     # ???
    return d

def test_3():
    CF = [[105, 0, 0], [6, 106, 0], [7, 7, 107]]
    B = [99.5, 101.25, 100.35]
    print(bootstrap(CF, B))
    # [[0.94761905]
    #  [0.90154987]
    #  [0.8168768]]

def test_2():
    # example with normal (coupon) bond
    times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cashflows = [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 1040.0]
    print(bond_duration(times, cashflows, 0.035)) # rate of 7% per year
    # 8.4723105333131112

    # another example with normal (coupon) bond
    cashflows = [70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 1070.0]
    print(bond_duration(times, cashflows, 0.035)) # rate of 7% per year
    # 7.843182123763313

    # example with a zero-coupon bond
    cashflows = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000]
    print(bond_duration(times, cashflows, 0.035)) # rate of 7% per year
    # 10.0

def test_1():
    times = [1, 2, 3]
    cashflows = [10, 10, 110]
    rate = 0.10
    print(bond_price(times, cashflows, rate))
    # 99.99999999999997

    rate = 0.085
    print(bond_price(times, cashflows, rate))
    # 103.8310335571048






