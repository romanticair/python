#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# a9task1.py
# name:
# e-mail:
"""

import numpy as np

# 1
def bond_price(times, cashflows, rate):
    """
    times is a list of the times at which the cashflows occur;
    cashflows is a list of the cashflows for this bond;
    r is the periodic (not annual) discount rate.
    returns the price of a bond
    """

    # 先看一下我在下面test里对本题的解释，就明白题目的意思了
    # 再结合网页上题目里提示的计算步骤，一步步实现就不难了

    d = [1/(1+rate)**t for t in times]  # 贴现因子列表
    #d = 1/ ( 1 + rate) ** np.array(times)  # 这句和上面那句的功能是一样的，只是得到的是array

    cf = np.matrix(cashflows) # 把列表cashflows变成矩阵，这样才能在下面做转置并与列表d相乘

    p = d * cf.T  # p:债券的价格矩阵（网页删公式中的T表示的是矩阵转置，即cf.T）

    # 矩阵转置：用矩阵的转置方法 .T
    # 上面得到的 p 是个矩阵，所以下面p[0,0]把矩阵的值取出来并返回
    # 取矩阵中元素的值：矩阵名[行索引,列索引]

    return p[0,0]

    # 通过这个题目掌握：1、列表转换成矩阵np.matrix(list)；2、矩阵的转置.T

#  #test 1
#>>> times = [1,2,3]
#>>> cashflows = [10,10,110]
#>>> rate = 0.10
#>>> bond_price(times, cashflows, rate)
#99.99999999999997
## 这个题目的意思是：已知债券的现金流时间列表times（例如上面的，共有3期）
## 还已知每期的现金流如cashflows中所示，分别是10，10，110
## 还已知利率rate是0.10
## 要求我们反过来算出这个债券最初的价值是多少。
#
## 我们算出来是$99.99999999999997即$100
## 也就是说这个债券当初是$100元发售的，每期的利率rate是0.10
## 分3期支付，那么每期的利息是$10（最后一期本息一起支付，所以是$110）
##
#>>> rate = 0.085
#>>> bond_price(times, cashflows, rate)
#103.8310335571048


# 2
def bond_duration(times, cashflows, rate):
    """
    times is a list of the times at which the cashflows occur;
    cashflows is a list of the cashflows for this bond;
    r is the periodic (not annual) discount rate.
    return the duration metric for a bond.
    """
    B = bond_price(times, cashflows, rate)  # B is the price of the bond
    t = np.array(times)  # t is an np.array of the times

    C = np.array(cashflows)  # C is a np.array of the bonds’ cashflows
    # 题目里说：C is a np.matrix... ，应该是错了
    # 因为下面D = (1/B) * t * C * d.T 语句中 t*C的话，array 不能与 matrix 相乘

    # 知识点：
    # 1、两个列表不能做相乘运算。
    # 如果想要两个列表对应元素相乘，需要先将列表转换成np.array。即np.array(list)
    # 2、list或np.array都可以和一个矩阵相乘，条件是其维度必须是对齐的
    # 即list或np.array的维度是(i,j)的话，矩阵的维度必须是(j,i)

    d = [1/(1+rate)**t for t in times]  # 贴现因子列表，用第1题里的公式求出
    #d = 1/ ( 1 + rate) ** np.array(times)  # 这句和上面那句的功能是一样的
    d = np.matrix(d)  # d is a np.matrix of discount factors ，题目里说是array，也错了

    D = (1/B) * t * C * d.T

    return D[0, 0]


 #test 2
#>>> # example with normal (coupon) bond
#>>> times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#>>> cashflows = [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 1040.0]
#>>> bond_duration(times, cashflows, 0.035)
#8.4723105333131112
#
#>>> # another example with normal (coupon) bond
#>>> times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#>>> cashflows = [70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 1070.0] #题目里变量名少了个's'
#>>> bond_duration(times, cashflows, 0.035) # rate of 7% per year
#7.843182123763313
#
#>>> # example with a zero-coupon bond:
#>>> times = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#>>> cashflows = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000]
#>>> bond_duration(times, cashflows, 0.035) # rate of 7% per year
#10.0


# 3
def bootstrap(cashflows, prices):
    """
    cashflows： is a matrix (2-dimensional list) containing the cashflows for some bonds
    prices:  is a column matrix (2-dimensional list) containing the prices of these bonds
    """

    P = np.matrix(prices) # P is a matrix containing the price of the bond
    CF = np.matrix(cashflows)  # CF is the matrix of the bonds’ cashflows

    # 使用 numpy.linalg.inv() 函数来计算矩阵的逆
    # We can find the prices of the implied zero-coupon bonds (i.e., discount factors) using this equation:
    #    d = CF**-1 * P
    d = CF**-1 * P.T  # d is the matrix of implied discount factors

    # 题目里说：You may use a list comprehension to create the list of discount factors.
    # 没搞懂为什么要这么做。把P转置一下(P.T)，然后用在上面这个计算d的公式里，测试得到了正确的结果

    # 题目里说prices is a colum matrix(2-dimensional list),但下面的测试里的B却是一个1-dimensional list
    # 我的理解是，形参prices(对应下面的实参B)就应该是个1-dimensional list的

    return d


# #test 3
>>> CF = [[105,0,0],[6,106,0],[7,7,107]]
>>> B = [99.5, 101.25, 100.35]
#>>> bootstrap(CF, B)
#matrix([[ 0.94761905],
#        [ 0.90154987],
#        [ 0.8168768 ]])


