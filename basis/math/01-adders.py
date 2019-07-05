def adder1(*args):
    print('adder1 ', end='')
    if isinstance(args[0], int):
        sum = 0
    else:
        sum = args[0][:0]
    for arg in args:
        sum += arg
    return sum


def adder2(*args):
    print('adder2 ', end='')
    sum = args[0]
    for arg in args[1:]:
        sum += arg
    return sum


if __name__ == '__main__':
    for func in (adder1, adder2):
        print(func(2, 3, 4))
        print(func('spam', 'eggs', 'toast'))
        print(func(['a', 'b'], ['c', 'd'], ['e', 'f']))
