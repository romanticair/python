from datetime import datetime
import re
"""
学习内置库 datetime
1. datetime 表示的时间需要时区信息才能确定一个特定的时间, 否则只能视为本地时间.
2. 如果要存储 datetime, 最佳方法是将其转换为 timestamp 再存储, 因为 timestamp 的值
  与时区完全无关.
"""

# 1
now = datetime.now()  # 获取当前日期和时间
print(now)  # 2018-02-05 21:40:23.730894
print(type(now))  # <class 'datetime.datetime'> 注意导入的方式

# 2
dt = datetime(2015, 4, 19, 12, 20)  # 用指定日期时间创建datetime
print(dt)  # 2015-04-19 12:20:00

# 3
# datetime 转换为 timestamp
# 格林威治标准时间(1970年1月1日 00:00:00 UTC+00:00时区), 1970以前为负
# timestamp是相对1970(epoch time 0)的秒数, 与时区无关, 所有计算机任意时刻都相同
print(dt.timestamp())  # 1429417200.0

# 4
# timestamp 转换为 datetime
t = 1429417200.0
print(datetime.fromtimestamp(t))  # 2015-04-19 12:20:00

# 5
# timestamp 转换为 UTC标准时区的时间
print(datetime.fromtimestamp(t))  # 本地时间
# 2015-04-19 12:20:00
print(datetime.utcfromtimestamp(t))  # UTC标准时间
# 2015-04-19 04:20:00

# 6
# str 转换为 datetime
# 很多时候, 用户输入的日期和时间是字符串, 要处理日期和时间, 必须把str转换为datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')  # 日期时间格式
print(cday)  # 2015-06-01 18:19:59

# 7
# datetime 转换为 str
# 有了datetime对象, 要把它格式化为字符串显示给用户, 就需要转换为str
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))  # Mon, Feb 05 22:00

# 8
# datetime加减
# 导入timedelta类, 可以用+ 和 - 运算符直接操作
# timedelta轻易推算前几天和后几天的时刻
from datetime import timedelta
now = datetime.now()
print(now) # 2018-02-05 22:05:07.586372
print(now + timedelta(hours=10)) # 2018-02-06 08:05:07.586372
print(now - timedelta(days=1)) # 2018-02-04 22:05:07.586372
print(now + timedelta(days=2, hours=12)) # 2018-02-08 10:05:07.586372

# 9
# 本地时间 转化为 UTC时间
# 本地时间是指系统设定时区的时间
# 如北京时间是UTC+8:00时区的时间, 而UTC时间指UTC+0:00时区的时间
# datetime类有个时区属性tzinfo, 默认为None, 要强制给datetime设时区才确定为哪个时区
from datetime import timezone
tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
now = datetime.now()
print(now) # 2018-02-05 22:12:01.415756
dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
print(dt) # 2018-02-05 22:12:01.415756+08:00

# 10
# 时区转换
# 可以先通过utcnow()拿到当前的UTC时间, 再转换为任意时区的时间
# 拿到UTC时间, 并强制设置时区为UTC+0:00
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt) # 2018-02-05 14:18:41.730485+00:00

# astimezone()将转换时区为北京时间
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt) # 2018-02-05 22:21:26.239638+08:00

# astimezone()将转换时区为东京时间
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt) # 2018-02-05 23:21:26.239638+09:00

# astimezone()将bj_dt转换时区为东京时间
tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt2) # 2018-02-05 23:21:26.239638+09:00


def to_timestamp(dt_str, tz_str):
    """
    test:

    获取了用户输入的日期和时间如 2015-6-21 9:01:30, 以及一个时区信息如 UTC+5:00,
    均是 str, 编写一个函数将其转换为 timestamp.
    """
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')  # 转为datetime
    tz = int(re.match(r'UTC([+-]\d+)', tz_str).group(1))  # 获取时区
    my_tz = timezone(timedelta(hours=tz))
    utc = dt.replace(tzinfo=my_tz)  # 强制转换为tz时区
    return utc.timestamp()

if __name__ == '__main__':
    t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
    assert t1 == 1433121030.0, t1
    t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
    assert t2 == 1433121030.0, t2
    print('ok')
