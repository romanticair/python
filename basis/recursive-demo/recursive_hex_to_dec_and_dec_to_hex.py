def hexToDecimal(hexString):
    if len(hexString) == 1:
        return int(hexString[0])
    else:
        return int(hexString[0]) * 16 ** (len(hexString) - 1) \
                + hexToDecimal(hexString[1:])


def decimalToHex(value):
    length = len(str(value))
    if value < 10:
        return value
    return 16 ** (length - 1) * (value // (10 ** (length - 1))) \
             + decimalToHex(value % (10 * (length - 1)))


if __name__ == '__main__':
    print(decimalToHex(12))
    print(hexToDecimal('12'))
