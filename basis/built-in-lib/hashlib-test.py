"""
hashlib 提供了常见的摘要算法，如 MD5，SHA1 等
摘要算法又称哈希算法、散列算法。它通过一个函数，
把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）

摘要算法之所以能指出数据是否被篡改过，就是因为摘要函数是一个单向函数，
计算 f(data) 很容易，但通过 digest 反推 data 却非常困难。

注意：摘要算法不是加密算法，不能用于加
密（因为无法通过摘要反推明文），只能用于防篡改，
但是它的单向计算特性决定了可以在不存储明文口令的情况下验证用户口令
"""
import hashlib
import random

# 1.MD5
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())  # d26a53750bc40b38b65a520292f69306
# 如果数据量很大，可以分块多次调用 update()，最后计算的结果是一样的

# 分块
md5 = hashlib.md5()
md5.update('how to use md5 in '.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())  # d26a53750bc40b38b65a520292f69306

# 改动一个字母，看看计算的结果
md5 = hashlib.md5()
md5.update('how to use md5 in Python hashlib?'.encode('utf-8'))
print(md5.hexdigest())  # 577361e734741bb6dfd97891d134c294
# MD5是最常见的摘要算法，速度很快，生成结果是固定的128 bit字节
# 通常用一个32位的16进制字符串表示。

# 2.SHA1
sha1 = hashlib.sha1()
sha1.update('how to use sha1 in '.encode('utf-8'))
sha1.update('python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())  # 2c76b57293ce30acef38d98f6046927161b46a44
# SHA1 的结果是160 bit字节，通常用一个40位的16进制字符串表示
# 比 SHA1 更安全的算法是 SHA256 和 SHA512，不过越安全的算法不仅越慢，而且摘要长度更长


def calc_md5(password):
    """根据用户输入的口令，计算出存储在数据库中的MD5口令"""
    md5_password = hashlib.md5()
    md5_password.update(password.encode('utf-8'))
    return md5_password.hexdigest()


def login(user, password):
    """设计一个验证用户登录的函数，根据用户输入的口令是否正确，返回 True 或 False"""
    if db[user] == calc_md5(password):
        return True
    return False

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}
# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')

# 根据用户输入的登录名和口令模拟用户注册，计算更安全的MD5
# 然后，根据修改后的 MD5 算法实现用户登录的验证


def register(username, password):
    db[username] = get_md5(password + username + 'the-Salt')
    return True


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = get_md5(password + self.salt)


def login(username, password):
    user = db[username]
    return user.password == get_md5(password + user.salt)

db = { 'michael': User('michael', '123456'),
       'bob': User('bob', 'abc999'),
       'alice': User('alice', 'alice2008')}
# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
