def adder1(*args):
    tot = args[0]
    for arg in args[1:]:
        tot += arg
    return tot


def adder2(**args):
    argskeys = list(args.keys())
    tot = args[argskeys[0]]
    for key in argskeys[1:]:
        tot += args[key]
    return tot


def adder3(**args):
    args = list(args.values())
    tot = args[0]
    for arg in args[1:]:
        tot += arg
    return tot


def adder4(**args):
    return adder1(*args.values())


print(adder1(1, 2, 3), adder1('aa', 'bb', 'cc'))
print(adder2(a=1, b=2, c=3), adder2(a='aa', b='bb', c='cc'))
print(adder3(a=1, b=2, c=3), adder3(a='aa', b='bb', c='cc'))
print(adder4(a=1, b=2, c=3), adder4(a='aa', b='bb', c='cc'))


