def gcd(m, n):
    # 求最大公约数
    if  m % n == 0:
        return n
    return gcd(n, m % n)

if __name__ == '__main__':
    print(gcd(48, 9))
