# 1
def numberSquare(n):
    # compute the square of 2
    if n == 0:
        return 1

    return 2 * numberSquare(n - 1)


def numberX_Square(x, n):
    # compute the square of x
    if x == 0:
        return 0
    if n == 0:
        return 1

    return x * numberX_Square(x, n - 1)


def main():
    n = eval(input("Enter a nonnegative interger: "))
    print("Factorial of ", n, "is ", factorial(n))


# 2
def f(n):
    if n == 1:
        return 1
    else:
        return n + f(n - 1)


def f2(n):
    if n < 10:
        return 0
    print(n % 10)
    f2(n // 10)


def main(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return main(n - 1) + main(n - 2)

def factorial(n):
    if n == 0:  # Base case
        return 1
    else:
        return n * factorial(n - 1)     # Recursive call

if __name__ == '__main__':
    main()
    print(f2(1234567))
