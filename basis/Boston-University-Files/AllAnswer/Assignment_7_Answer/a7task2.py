from a7task1 import Date


def options_expiration_days(n):
    """
    Return a list of all of the Dates on which
    options expire during a calendar year.

    Here is the expire on the third Friday
    of the month

    """
    expireList = []
    weekCount = 0
    dateObject = Date(1, 1, n)
    while dateObject.month < 13:
        if dateObject.day_of_week() == "Friday":
            weekCount += 1
        if weekCount == 3:
            expireList.append(dateObject.copy())
            dateObject.month += 1
            dateObject.day = 1
            weekCount = 0
            continue
        dateObject.add_one_day()

    print(expireList)

def market_holiday(year):
    """
    Return a list of the Dates of all market
    holidays for a given year

    And print each holiday
    """
    dateList = []
    NewYear = Date(1, 1, year)
    MartinLutherKing = Date(1, 1, year)
    President = Date(2, 1, year)
    Memorial = Date(5, 1, year)
    Independence = Date(7, 4, year)
    Labor = Date(9, 1, year)
    Thanksgiving = Date(11, 1, year)
    Christma = Date(12, 25, year)
    tags = 0   # 3 -> 6 -> 10 分别代表日期可选取

    # 以下分别对各日期进行选取
    if NewYear.day_of_week() == "Sunday":
        NewYear.day += 1
        dateList.append(NewYear)
    else:
        dateList.append(NewYear)

    while True:
        if MartinLutherKing.day_of_week() == "Monday":
            tags += 1
            if tags == 3:
                dateList.append(MartinLutherKing)
                break
        MartinLutherKing.day += 1

    while True:
        if President.day_of_week() == 'Monday':
            tags += 1
            if tags == 6:
                dateList.append(President)
                break
        President.day += 1

    while True:
        if Memorial.day_of_week() == "Monday":
            if Memorial.day + 7 > 31:
                dateList.append(Memorial)
                break
        Memorial.day += 1

    if Independence.day_of_week() == "Sunday":
        Independence.day += 1
        dateList.append(Independence)
    else:
        dateList.append(Independence)

    while True:
        if Labor.day_of_week() == "Monday":
            dateList.append(Labor)
            break
        Labor.day += 1

    while True:
        if Thanksgiving.day_of_week() == "Thursday":
            tags += 1
            if tags == 10:
                dateList.append(Thanksgiving)
                break
        Thanksgiving.day += 1

    if Christma.day_of_week() == "Sunday":
        Christma.day += 1
        dateList.append(Christma)
    else:
        dateList.append(Christma)

    DATELIST = [NewYear] + [MartinLutherKing] + [President] + [Memorial] + [Independence] + [Labor] \
               + [Thanksgiving] + [Christma]
    observeList = ['New Year\'s', 'Martin Luther King', 'President\'s', 'Memorial Day', 'Independence Day', \
                   'Labor Day', 'Thanksgiving Day', 'Christmas Day']
    # Print
    for i in range(8):
        print(observeList[i], " Day is observed on ", DATELIST[i].day_of_week(), ' -> ', dateList[i])

    return dateList


if __name__ == '__main__':
    # Test options_expiration_days(n) #
    options_expiration_days(2017)
    print()
    # [01/20/2017, 02/17/2017, 03/17/2017, 04/21/2017, 05/19/2017, 06/16/2017,
    # 07/21/2017, 08/18/2017,#  09/15/2017, 10/20/2017, 11/17/2017, 12/15/2017] #

    options_expiration_days(2018)
    print()
    # [01/19/2018, 02/16/2018, 03/16/2018, 04/20/2018, 05/18/2018, 06/15/2018,
    #  07/20/2018, 08/17/2018, 09/21/2018, 10/19/2018, 11/16/2018, 12/21/2018] #

    # Test market_holiday(year) #
    d1 = market_holiday(2017)
    print(d1)
    print()
    """
        New Year's  Day is observed on  Monday  ->  01/02/2017
        Martin Luther King  Day is observed on  Monday  ->  01/16/2017
        President's  Day is observed on  Monday  ->  02/20/2017
        Memorial Day  Day is observed on  Monday  ->  05/29/2017
        Independence Day  Day is observed on  Tuesday  ->  07/04/2017
        Labor Day  Day is observed on  Monday  ->  09/04/2017
        Thanksgiving Day  Day is observed on  Thursday  ->  11/23/2017
        Christmas Day  Day is observed on  Monday  ->  12/25/2017
        [01/02/2017, 01/16/2017, 02/20/2017, 05/29/2017,
         07/04/2017, 09/04/2017, 11/23/2017, 12/25/2017]

    """

    d1 = market_holiday(2018)
    print(d1)
    """
        New Year's  Day is observed on  Monday  ->  01/01/2018
        Martin Luther King  Day is observed on  Monday  ->  01/15/2018
        President's  Day is observed on  Monday  ->  02/19/2018
        Memorial Day  Day is observed on  Monday  ->  05/28/2018
        Independence Day  Day is observed on  Wednesday  ->  07/04/2018
        Labor Day  Day is observed on  Monday  ->  09/03/2018
        Thanksgiving Day  Day is observed on  Thursday  ->  11/22/2018
        Christmas Day  Day is observed on  Tuesday  ->  12/25/2018
        [01/01/2018, 01/15/2018, 02/19/2018, 05/28/2018,
        07/04/2018, 09/03/2018, 11/22/2018, 12/25/2018]

    """




















