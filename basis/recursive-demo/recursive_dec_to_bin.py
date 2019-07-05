# Function transfer decimal value to binary


def decimalToBinary(value):
    if value == 1:
        return '1'
    elif value == 0:
        return ''
    if value % 2 == 0:
        return decimalToBinary(value // 2) + '0'
    return decimalToBinary(value // 2) + '1'


if __name__ == '__main__':
    print(decimalToBinary(8))
