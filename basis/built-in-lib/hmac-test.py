"""
为了防止黑客通过彩虹表根据哈希值反推原始口令，在计算哈希的时候，不能仅针对原始输入计算，
需要增加一个 salt 来使得相同的输入也能得到不同的哈希，这样，大大增加了黑客破解的难度。

如果salt是我们自己随机生成的，通常我们计算MD5时采用md5(message + salt)。但实际上，
把salt看做一个“口令”，加salt的哈希就是：计算一段message的哈希时，根据不通口令计算
出不同的哈希。要验证哈希值，必须同时提供正确的口令。

这实际上就是Hmac算法：Keyed-Hashing for Message Authentication。它通过一个标准算法，
在计算哈希的过程中，把key混入计算过程中。和我们自定义的加salt算法不同，Hmac算法针对所
有哈希算法都通用，无论是MD5还是SHA-1。

使用 hmac 算法比标准 hash 算法更安全，因为针对相同的message，不同的 key 会产生不同的hash
"""
import hmac
import random

message = b'Hello, world!'
key = b'secret'
h = hmac.new(key, message, digestmod='MD5')  # 如果消息很长，可以多次调用h.update(msg)
print(h.hexdigest())  # 'fa4ee7d173f2d97ee79022d1a7355bcf'

# 可见使用 hmac 和普通 hash 算法非常类似。hmac 输出的长度和原始哈希算法的长度一致,
# 需要注意传入的 ke y和 message 都是 bytes 类型，str 类型需要首先编码为 bytes


def hmac_md5(key, s):
    """将 salt 改为标准的 hmac 算法，验证用户口令"""
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = hmac_md5(self.key, password)


def login(username, password):
    user = db[username]
    return user.password == hmac_md5(user.key, password)

db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}
# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
