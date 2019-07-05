"""
虽然Python提供了Unicode表示的str和bytes两种数据类型
但是，在不知道编码的情况下，对bytes做decode()不好做

用第三方库chardet来检测编码, 简单易用
当我们拿到一个bytes时，就可以对其检测编码。用chardet检测编码

用chardet检测编码，获取到编码后，再转换为str，就可以方便后续处理
"""
import chardet

print(chardet.detect(b'Hello, world!'))
# {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
# 检测出的编码是ascii，注意到还有个confidence字段，表示检测的概率是1.0（即100%）

# 检测GBK编码的中文
data = '离离原上草， 一岁一枯荣'.encode('gbk')
print(chardet.detect(data))
# {'encoding': 'GB2312', 'language': 'Chinese', 'confidence': 0.7407407407407407}

# UTF-8编码进行检测
data = '离离原上草， 一岁一枯荣'.encode('utf-8')
print(chardet.detect(data))
# {'language': '', 'encoding': 'utf-8', 'confidence': 0.99}

# 对日文进行检测
data = '最新の主要ニュース'.encode('euc-jp')
print(chardet.detect(data))
# {'confidence': 0.99, 'language': 'Japanese', 'encoding': 'EUC-JP'}
