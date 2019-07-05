def prime(y):
    if y <= 1:
        print(y, ' not prime')
    else:
        x = y // 2
        while x > 1:
            if y % x == 0:
                print(y, ' has factor ', x)
                break
            x -= 1
        else:
            print(y, ' is prime')


if __name__ == '__main__':
    print(prime(13))
    print(prime(13.0))
    print(prime(15))
    print(prime(15.0))
    print(prime(3))
    print(prime(2))
    print(prime(1))
    print(prime(-3))



