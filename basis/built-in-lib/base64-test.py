"""
Base64 是一种用 64 个字符来表示任意二进制数据的方法
二进制数据需要一个二进制到字符串的转换方法, Base64 是一种最常见的二进制编码方法

Base64的原理很简单，首先，准备一个包含 64 个字符的数组
['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']
对二进制数据进行处理，每3个字节一组，一共是 3x8=24bit，划为 4 组，每组正好 6 个 bit
得到4  个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串
Base64 编码会把 3 字节的二进制数据编码为 4 字节的文本数据，长度增加 33%,
好处是编码后的文本数据可以在邮件正文、网页等直接显示.
"""
import base64

# 直接进行 base64 的编解码
print(base64.b64encode(b'binary\x00string'))  # b'YmluYXJ5AHN0cmluZw=='
print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))  # b'binary\x00string'

# 由于标准的 Base64 编码后可能出现字符 + 和 /, 在 URL 中就不能直接作为参数
# 所以又有一种"url safe"的 base64 编码, 其实就是把字符 + 和 / 分别变成 - 和 _
print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))  # b'abcd++//'
print(base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff'))  # b'abcd--__'
print(base64.urlsafe_b64decode('abcd--__'))  # b'i\xb7\x1d\xfb\xef\xff

# Base64 是一种通过查表的编码方法，不能用于加密，即使使用自定义的编码表也不行,
# Base64 适用于小段内容的编码，比如数字证书签名、Cookie 的内容等.

# 由于 = 字符也可能出现在 Base64 编码中, 但 = 用在 URL、Cookie 里面会造成歧义,
# 所以, 很多 Base64 编码后会把 = 去掉
# 标准Base64:
# 'abcd' -> 'YWJjZA=='
# 自动去掉 =
# 'abcd' -> 'YWJjZA'

# 因为 Base64 是把 3 个字节变为 4 个字节, 所以, Base64 编码的长度永远是 4 的倍数,
# 因此, 需要加上 = 把 Base64 字符串的长度变为 4 的倍数, 就可以正常解码了

# Base64 是一种任意二进制到文本字符串的编码方法,
# 常用于在URL、Cookie、网页中传输少量二进制数据


# 写一个能处理去掉 = 的 base64 解码函数

def safe_base64_decode(s):  # 1
    # 判断传入的是bytes还是string
    if type(s) is bytes:
        s = str(s, encoding='utf-8')
    if len(s) % 4 == 0:
        return base64.b64decode(s)
    s = s + str((4 - len(s)%4) * '=')
    return base64.b64decode(s)


def safe_base64_decode2(s):  # 2
    # 判断传入的是bytes还是string
    if type(s) is bytes:
        if len(s) % 4 == 0:
            return base64.b64decode(s)
        s = s + (4 - len(s)%4) * b'='
        return base64.b64decode(s)


def safe_base64_decode3(s):  # 3
    # Recursive
    if len(s) % 4  == 0:
        return base64.b64decode(s)
    return safe_base64_decode3(s + b'=')


# 测试:
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('ok')

s = base64.b64encode('在Python中使用BASE 64编码'.encode('utf-8'))
print(s)
d = base64.b64decode(s).decode('utf-8')
print(d)

s = base64.urlsafe_b64encode('在Python中使用BASE 64编码'.encode('utf-8'))
print(s)
d = base64.urlsafe_b64decode(s).decode('utf-8')
print(d)
