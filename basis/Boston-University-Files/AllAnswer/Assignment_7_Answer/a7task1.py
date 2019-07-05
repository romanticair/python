

# 创建一个时间日期类
class Date:
    def __init__(self, new_month, new_day, new_year):
        self.month = new_month
        self.day = new_day
        self.year = new_year

    def __repr__(self):
        return "{0:02}/{1:02}/{2:04}".format(self.month, self.day, self.year)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.month == other.month and\
                 self.day == other.day and\
                 self.year == other.year)

    def __lt__(self, other):
        return self.is_before(other)

    def __gt__(self, other):
        return self.is_after(other)

    def __add__(self, n):
        if not isinstance(n, int):
            print("Operator - is only defined for Date and int.")
        new = self.copy() # New object
        new.add_n_days(n)
        return new

    def __sub__(self, n):
        if not isinstance(n, int):
            print("Operator - is only defined for Date and int.")
        new = self.copy()
        new.rem_n_days(n)
        return new

    def __iadd__(self, n):
        if not isinstance(n, int):
            print("Operator += is only defined for Date and int.")
        self.add_n_days(n)
        return self

    def __isub__(self, n):
        if not isinstance(n, int):
            print("Operator -= is only defined for Date and int.")
        self.rem_n_days(n)
        return self

    def copy(self):
        return self.__class__(self.month, self.day, self.year)

    def is_leap_year(self):
        """
        Return true if the called object is a
        leap year, and False otherwise.

        """
        return self.year % 400 == 0 or (self.year % 4 == 0 and self.year % 100 != 0)

    def is_valid_date(self):
        """
        Return True if the object is a valid date,
        and False otherwise.

        """
        if 12 < self.month or self.month < 1 or self.year < 0:
            return False

        if self.month in (4, 6, 9, 11):
            return 1 <= self.day <= 30
        elif self.month == 2:
            if self.is_leap_year():  # Leap year
                    return 1 <= self.day <= 29
            else:                    # Normal year
                    return 1 <= self.day <= 28
        else:
            return 1 <= self.day <= 31

    def add_one_day(self):
        """
        Advancing one day Date object by itself
        return None

        """
        if not self.is_valid_date():
            return False

        normal_year_days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # The last day in month
        if self.day == normal_year_days_in_month[self.month]:
            if self.month == 12:  # The last month
                self.year += 1
                self.day = 1
                self.month = 1
            # Deal with the leap year in February
            elif self.month == 2 and self.is_leap_year():
                self.day = 29
            # Other month situation
            else:
                self.month += 1
                self.day = 1
        # Deal with the leap year in February
        elif self.month == 2 and self.day == 29 and self.is_leap_year():
            self.day = 1
            self.month = 3
        # Not the last day in month
        else:
            self.day += 1

    def rem_one_day(self):
        """
        Back one day Date object itself
        return None

        """
        if not self.is_valid_date():
            return False

        normal_year_days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # The first day in month
        if self.day == 1:
            if self.month == 1:  # The first month
                self.year -= 1
                self.day = 31
                self.month = 12
            # Deal with leap year in March to February
            elif self.is_leap_year() and self.month == 3:
                self.month -= 1
                self.day = 29
            else:
                self.month -= 1
                self.day = normal_year_days_in_month[self.month]
        else:
            self.day -= 1

    def add_n_days(self, n):
        """
        Change the values of Date object by Adding n days

        """
        assert n > -1 and str(n).isnumeric(), "n is not a useful value"
        for _ in range(n):
            self.add_one_day()

    def rem_n_days(self, n):
        """
        Change the values of Date object by Rem n days

        """
        assert n > -1 and str(n).isnumeric(), "n is not a useful value"
        for _ in range(n):
            self.rem_one_day()

    def is_before(self, other):
        """
        If self's calendar is earlier than others return True,
        and otherwise False.

        """
        if self.year < other.year:
            return True

        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month and self.day < other.day:
                return True
            else:
                return False

        else:
            return False

    def is_after(self, other):
        """
        If self's calendar is later than others return True,
        and otherwise False

        """
        return False if self == other else not self.is_before(other)

    def diff(self, other):
        """
        Return the different days between self and other objects

        """
        date = self.copy()
        n = 0
        while date.is_before(other):
            n -= 1
            date.add_one_day()
        while date.is_after(other):
            n += 1
            date.rem_one_day()
        return n

    def day_of_week(self):
        """
        Return the day of week name of self object.

        """
        day_of_week_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                             'Friday', 'Saturday', 'Sunday']
        Days = self.diff(Date(1, 14, 2018))  # 01/14/2018 is Sunday
        return day_of_week_names[Days % 7 - 1]


if __name__ == '__main__':
    # Task1 ::
    # Test1.1 __init__(self, new_month, new_day, new_year) and __repr__(self) methods #
    d1 = Date(10, 17, 2017)
    print(d1)
    # 10/17/2017

    # __eq__(self) and copy(self) methods #
    d1 = Date(10, 17, 2017)
    d2 = d1
    d3 = d1.copy()
    print(d1)  # 10/17/2017
    print(id(d1), id(d2), id(d3))  # 67416880 67416880 62151440
    print(d1 == d2, d1 == d3)
    # True True     已用后面的值相等判断方法，而不用内存值

    # Test1.2 is_leap_year(self) method #
    d1 = Date(1, 1, 2016)
    d2 = Date(1, 1, 2017)
    print(d1.is_leap_year(), d2.is_leap_year())
    # True False

    d3 = Date(1, 1, 2000)
    d4 = Date(1, 1, 1900)
    print(d3.is_leap_year(), d4.is_leap_year())
    # True False

    # Test1.3 is_valid_date(self) method #
    d1 = Date(10, 7, 2017)
    d2 = Date(14, 2, 2017)
    d3 = Date(2, 30, 2017)
    print(d1.is_valid_date(), d2.is_valid_date(), d3.is_valid_date())
    # True False False

    d4 = Date(2, 29, 2016)
    d5 = Date(2, 29, 2017)
    d6 = Date(-4, -4, -5)
    d7 = Date(2, 29, 1900)
    print(d4.is_valid_date(), d5.is_valid_date(), d6.is_valid_date(), d7.is_valid_date())
    # True False False False

    # Test1.4 add_one_day(self) method #
    d1 = Date(12, 31, 2017)
    print(d1, " -> ", end = "")
    d1.add_one_day()
    print(d1)
    # 12/31/2017 -> 01/01/2018

    d2 = Date(2, 28, 2016)
    print(d2, " -> ", end = "")
    d2.add_one_day()
    print(d2, " -> ", end = "")
    d2.add_one_day()
    print(d2)
    # 02/28/2016 -> 02/29/2016 -> 03/01/2016

    # Test1.5 rem_on_day(self) method #
    d1 = Date(3, 1, 2017)
    print(d1, " -> ", end = "")
    d1.rem_one_day()
    print(d1)
    # 03/01/2017 -> 02/28/2017

    d2 = Date(3, 2, 2016)
    print(d2, " -> ", end="")
    d2.rem_one_day()
    print(d2, " -> ", end="")
    d2.rem_one_day()
    print(d2)
    # 03/02/2016 -> 03/01/2016 -> 02/29/2016

    d3 = Date(1, 1, 2015)
    print(d3, " -> ", end="")
    d3.rem_one_day()
    print(d3)
    # 01/01/2015 -> 12/31/2014

    # Test1.6 add_n_days(self, n) method #
    d = Date(10, 17, 2017)
    d.add_n_days(3)
    print(d)
    # 10/20/2017

    d = Date(10, 17, 2017)
    d.add_n_days(0)
    print(d)
    # 10/17/2017

    # Test1.7 rem_n_days #
    d = Date(10, 17, 2017)
    d.rem_n_days(3)
    print(d)
    # 10/14/2017

    d = Date(10, 17, 2017)
    d.rem_n_days(0)
    print(d)
    # 10/17/2017

    # Test1.8 __eq__(self, other) method #
    d1 = Date(1, 1, 2018)
    d2 = d1
    d3 = d1.copy()
    print(id(d1), id(d2), id(d3))  # 67416944 67416944 67417072
    print(d1 == d2, d1 == d3)
    # True True

    # Test1.9 is_before(self, other) method #
    ny = Date(1, 1, 2018)
    d = Date(10, 17, 2017)
    print(ny.is_before(d))  # False
    print(d.is_before(ny))  # True
    print(d.is_before(d))  # False

    d3 = Date(12, 21, 2017)
    print(d3.is_before(ny))  # True
    d4 = Date(12, 31, 2018)
    print(d4.is_before(ny))  # False

    # Test1.10 is_after(self, other) method #
    ny = Date(1, 1, 2018)
    d3 = Date(12, 31, 2017)
    print(d3.is_after(ny))  # False

    d4 = Date(12, 31, 2018)
    print(d4.is_after(ny))  # True

    # Test1.11 diff(self, other) method #
    d1 = Date(10, 17, 2017)
    d2 = Date(4, 16, 2018)
    print(d2.diff(d1))  # 181
    print(d1.diff(d2))  # -181
    print(d1)  # 10/17/2017
    print(d2)  # 04/16/2018

    d3 = Date(12, 1, 2015)
    d4 = Date(3, 15, 2016)
    print(d4.diff(d3))  # 105

    d3 = Date(12, 1, 2015)
    d4 = Date(12, 1, 2016)
    print(d4.diff(d3))  # 366

    # Test1.12 day_of_week(self) method #
    d = Date(4, 16, 2018)
    print(d.day_of_week())  # 'Monday'
    print(Date(1, 1, 2100).day_of_week())  # 'Friday'
    print(Date(7, 4, 1776).day_of_week())  # 'Thursday'
    print(Date(1, 14, 2018).day_of_week())  # 'Sunday'


# Task2::
    # Test2.1 __lt__(self, other) and __gt__(self, other) methods #
    d1 = Date(4, 16, 2018)
    d2 = Date(10, 17, 2017)
    print(d1 < d2)  # False
    print(d2 < d1)  # True
    print(d1 > d2)  # True
    print(d2 > d1)  # False

    # Test2.2 __add__(self, n) and __sub__(self, n) methods #
    d1 = Date(10, 17, 2017)
    d2 = d1 + 181
    print(d1)  # 10/17/2017
    print(d2)  # 04/16/2018
    d3 = d2 - 181
    print(d3)  # 10/17/2017

    # Test2.3 __iadd__(self, n) and __isub__(self, n) methods #
    d1 = Date(10, 17, 2017)
    d1 += 181
    print(d1)  # 04/16/2018
    d1 -= 181
    print(d1)  # 10/17/2017

    d = Date(1, 1, 2017)
    d += 1
    print(d)  # 01/02/2017

    d += 1.2
    print(d)
    # Operator += is only defined for Date and int
