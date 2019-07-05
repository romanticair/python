# Task 4 :Functions for time value of money caculations

def fv_lump_sum(r, n, pv):
    # return the future value of pv inversted at the periodic
    # rate r for n periods.
    return pv * (1 + r) ** n

# $100 at 5% rate for 2 years -> 110.25
# print(fv_lump_sum(0.05, 2, 100))

def pv_lump_sum(r, n, fv):
    # return the present value of a fv to be received
    # in the future
    return fv / (1 + r) ** n

# $1000 to be received in 5 years at 6% per year ->747
# print(pv_lump_sum(0.06, 5, 1000))

def pv_annuity(r, n, pmt):
    # return the present value of an annuity of pmt to be
    # received each period for n periods
    return pmt * ((1 - (1 + r) ** (- n)) / r)

# pv of 30 payments of $250 per yearr, 5% interest
# print(pv_annuity(0.05, 30, 250))

def pmt_annuity(r, n, pv):
    # return the amortizing loan payment for a present value
    # of pv to be repaid at a periodic interest rate for r for n periods.
    return r * pv / (1 - (1 + r) ** (- n))

# loan payment for pv of #1,000 for 10 year at 5%
# print(pmt_annuity(0.05, 10, 1000))

