# Descriptive Statistice

# Mission 1.
def mean(values):
    # Take as a parameter a list of numbers, calculates4
    # and returns the mean of those values
    sumValues = 0
    for value in values:
        sumValues += value
    return sumValues / len(values)

# Mission 2.
def variance(values):
    # Take as a parameter a list of numbers, calculated
    # and returns the population variance of the values
    # in the list. which was defined as :
    # o² = (1 / N) * ∑(Xi - u)²
    u = mean(values)
    deviation = 0
    for value in values:
        deviation += (value - u) ** 2
    return deviation / len(values)


# Mission 3.
def stdev(values):
    # Takes as parameter a list of numbers, calculates
    # and returns the popution standard deviation of the
    # values in the list, which was the square-root of the
    # population variance.
    return variance(values) ** 0.5

# Mission 4.
def covariance(x, y):
    # Takes as parameters two lists of values, calculates
    # and returns the population covariance for those two
    # list, which was defined as :
    # Oxy = (1 / N) * ∑(Xi - Ux)(Yi - Uy)
    assert len(x) == len(y), print("Two lists length is'nt equal")
    Ux = mean(x)
    Uy = mean(y)
    twoDeviation = 0
    for i in range(len(x)):
      twoDeviation += (x[i] - Ux) * (y[i] - Uy)

    return twoDeviation / len(x)

# Mission 5.
def correlation(x, y):
    # Takes as parameters two lists of values,calculates
    # and returns the correlation coefficient between
    # these data series, which was defined as:
    # Pxy = Oxy / (Ox * Oy)
    Ox = stdev(x)
    Oy = stdev(y)
    Oxy = covariance(x, y)
    return Oxy / (Ox * Oy)

# Mission 6.
def rsq(x, y):
    # Takes as parameters two lists of values,calculates
    # and returns the square of the coefficient between
    # those two data series, which is a measure of the
    # goodness of fit measure to explain variation in
    # y as a function of variation of x
    return correlation(x, y) ** 2

# Mission 7
def simple_regression(x, y):
    # Take as parameters two lists of values, calculate
    # the regreesion coefficients between these data series,
    # and return a list containing two values: the intercept
    # and regression coefficients, A and B
    # Bxy = Oxy / Ox²,  Axy = Uy - Bxy * Ux
    Oxy = covariance(x, y)
    Ox = stdev(x)
    Oy = stdev(y)
    Ux = mean(x)
    Uy = mean(y)
    Bxy = Oxy / (Ox ** 2)
    Axy = Uy - Bxy * Ux
    return [Axy, Bxy]

def Test():
    x = [4, 4, 3, 6, 7]
    y = [6, 7, 5, 10, 12]
    print(mean(x))
    print(variance(x))
    print(stdev(x))
    print(covariance(x, y))
    print(correlation(x, y))
    print(correlation(list(range(10)), list(range(10, 0, -1))))
    print(rsq(x, y))
    print(simple_regression(x, y))
    """
    Test :
    import random
    a = list(range(30))
    b = list(range(30))
    random.shuffle(a)
    random.shuffle(b)
    print(correlation(a, b))
    print(rsq(a, b))

    """







