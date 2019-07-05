def decimalToHex(value):
    if value < 16:
        return '0x ' + str(number_to_letter(value))
    return decimalToHex(value // 16) + str(number_to_letter(value % 16))


def number_to_letter(n):
    if n > 9:
        return chr(87 + n).upper()
    else:
        return n

if __name__ == '__main__':
    print(decimalToHex(10))
