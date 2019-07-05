# -*- coding: utf-8 -*-
"""
# a8task2.py
# name: 
# e-mail: 
"""

import random
import statistics
import math


# 1
class MCStockOption:
    """
    input:
        s, which is the initial stock price
        x, which is the option’s exercise price
        r, which is the (expected) mean annual rate of return on the underlying stock
        sigma, which is the annual standard deviation of returns on the underlying stock
        t, which is the time to maturity for the option
        nsteps, which is the number of discrete time steps with which to evaluate the option
        ntrials, which is the number of trials to run with this option
    """

    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        self.s = s
        self.x = x
        self.r = r
        self.sigma = sigma
        self.t = t
        self.nsteps = nsteps
        self.ntrials = ntrials

    def __repr__(self):
        return "MCStockOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)

    # 2
    def generate_stock_prices(self):
        """
        return:  generate and return a list containing simulated
            stock prices over the course of this option’s lifetime t
        """

        dt = self.t / self.nsteps

        ret_list = [self.s]

        for i in range(self.nsteps):
            z = random.gauss(0, 1)
            # Z is a randomly-drawn number from the standard normal distribution.
            # You can draw such a number using the function random.gauss(mu, sigma).
            E_r = (self.r - self.sigma ** 2 / 2) * dt + z * self.sigma * math.sqrt(dt)

            price = ret_list[-1] * math.exp(E_r)
            ret_list.append(price)

        return ret_list

    # 3
    # a
    def value(self):  #
        """
          return the value of the option
        """
        print("Base class MCStockOption has no concrete implementation of .value().")
        return 0

    # b
    def stderr(self):
        """
        return the standard error of this option’s value.
        """
        if 'stdev' in dir(self):
            return self.stdev / math.sqrt(self.ntrials)
        return 0


# 4
class MCEuroCallOption(MCStockOption):
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        self.mean = 0
        self.stdev = 0

    def value(self):
        trials = []
        for i in range(self.ntrials):
            trials_path = self.generate_stock_prices()
            C = max(trials_path[-1] - self.x, 0) * math.e ** (-self.r * self.t)
            trials.append(C)

        self.mean = statistics.mean(trials)
        self.stdev = statistics.pstdev(trials)

        return self.mean

    def __repr__(self):
        return "MCEuroCallOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)


# 5
class MCEuroPutOption(MCStockOption):
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        self.mean = 0
        self.stdev = 0

    def value(self):
        trials = []
        for i in range(self.ntrials):
            trials_path = self.generate_stock_prices()
            P = max(self.x - trials_path[-1], 0) * math.e ** (-self.r * self.t)
            trials.append(P)

        self.mean = statistics.mean(trials)
        self.stdev = statistics.pstdev(trials)

        return self.mean

    def __repr__(self):
        return "MCEuroPutOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)


# 6
class MCAsianCallOption(MCStockOption):
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        self.mean = 0
        self.stdev = 0

    def value(self):
        trials = []
        for i in range(self.ntrials):
            trials_path = self.generate_stock_prices()
            C = max(statistics.mean(trials_path) - self.x, 0) * math.e ** (-self.r * self.t)
            trials.append(C)

        self.mean = statistics.mean(trials)
        self.stdev = statistics.pstdev(trials)

        return self.mean

    def __repr__(self):
        return "MCAsianCallOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)


# 7
class MCAsianPutOption(MCStockOption):
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        self.mean = 0
        self.stdev = 0

    def value(self):
        trials = []
        for i in range(self.ntrials):
            trials_path = self.generate_stock_prices()
            P = max(self.x - statistics.mean(trials_path), 0) * math.e ** (-self.r * self.t)
            trials.append(P)

        self.mean = statistics.mean(trials)
        self.stdev = statistics.pstdev(trials)

        return self.mean

    def __repr__(self):
        return "MCAsianPutOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)


# 8
class MCLookbackCallOption(MCStockOption):
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        self.mean = 0
        self.stdev = 0

    def value(self):
        trials = []
        for i in range(self.ntrials):
            trials_path = self.generate_stock_prices()
            C = max(max(trials_path) - self.x, 0) * math.e ** (-self.r * self.t)
            trials.append(C)

        self.mean = statistics.mean(trials)
        self.stdev = statistics.pstdev(trials)

        return self.mean

    def __repr__(self):
        return "MCLookbackCallOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)


# 9
class MCLookbackPutOption(MCStockOption):
    def __init__(self, s, x, r, sigma, t, nsteps, ntrials):
        MCStockOption.__init__(self, s, x, r, sigma, t, nsteps, ntrials)
        self.mean = 0
        self.stdev = 0

    def value(self):
        trials = []
        for i in range(self.ntrials):
            trials_path = self.generate_stock_prices()
            P = max(self.x - min(trials_path), 0) * math.e ** (-self.r * self.t)
            trials.append(P)

        self.mean = statistics.mean(trials)
        self.stdev = statistics.pstdev(trials)

        return self.mean

    def __repr__(self):
        return "MCLookbackPutOption, s=%7.2f, x=%7.2f, r=%4.2f, sigma=%4.2f, t=%3.2f, nsteps=%d, ntrials=%d" \
               % (self.s, self.x, self.r, self.sigma, self.t, self.nsteps, self.ntrials)

if __name__ == '__main__':
    import time
    ntrials = 1
    for i in range(7):
        ntrials = ntrials * 10
        lcall = MCLookbackCallOption(100, 100, 0.10, 0.30, 1, 100, ntrials)
        start = time.clock()
        print("ntrials=" , ntrials, " ,value=$", lcall.value(), " , stderr=$", lcall.stderr(), end='')
        end = time.clock()
        print(" ,time=", (end-start))  # clock()返回的时间单位是：秒










