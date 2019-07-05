"""地区天气数据统计可视化"""

import csv
from datetime import datetime
from matplotlib import pyplot as plt

"""
# 从文件中获取希特天气一个月内的最高气温
filename = 'sitka_weather_07-2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)         # 获取下一行
    print(header_row)                 # 这里是第一行(文件头),每个题头作为列表返回
    for index, column_header in enumerate(header_row):
        print(index, column_header)   # 将列表每个文件头及其位置打印出来

    dates, highs = [], []             # 日期, 最高温
    for row in reader:
        current_date = datetime.strptime(row[0], '%Y-%m-%d')
        dates.append(current_date)    # 获取日期(第一列)(日期已被格式化)
        high = int(row[1])            # 获取每天的最高气温(索引1第二列的意思)
        highs.append(high)
    print(highs)

# 根据数据绘制图形
fig = plt.figure(figsize=(10, 6), dpi=128)
plt.plot(dates, highs, c='red')              # 将数据点绘制成红色(红高温，篮低温)
# 设置图形的格式
plt.title('Daily high temperatures, July 2014', fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()                          # 绘制斜的日期标签(防止重叠)
plt.ylabel('Temperature (F)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()
"""

# 从文件中获取希特天气整年的日期，最高温度和最低气温
filename = 'sitka_weather_2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)        # 获取下一行
    for index, column_header in enumerate(header_row):
        print(index, column_header)  # 将列表每个文件头及其位置打印出来

    dates, highs, lows = [], [], []  # 日期, 最高温, 最低温
    for row in reader:
        try:                            # 获取日期(第一列)(日期已被格式化)
            current_date = datetime.strptime(row[0], '%Y-%m-%d')
            high = int(row[1])           # 获取每天的最高气温(索引1第二列的意思)
            low = int(row[3])            # 获取每天的最低气温(第四列)
        except ValueError:              # 缺失数据等错误检查
            print(current_date, 'missing data')
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

# 根据数据绘制图形
fig = plt.figure(figsize=(10, 6), dpi=128)
# plt.plot(dates, highs, c='red')      # 红最高温
# plt.plot(dates, lows, c='blue')      # 蓝最低温
plt.plot(dates, highs, c='red', alpha=0.5)      # alpha指定颜色的透明度
plt.plot(dates, lows, c='blue', alpha=0.5)      # 0表示完全透明, 默认1
# 着色修饰每天的气温范围, 它接受一个x值系列和两个y值系列，并填充两个y值间的空间
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
# 设置图形的格式
plt.title('Daily high temperatures - 2014', fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()                  # 绘制斜的日期标签(防止重叠)
plt.ylabel('Temperature (F)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()
