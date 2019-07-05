# transfer binary value to decimal


def binaryToDecimal(binaryString):
    if len(binaryString) == 1:
        return int(binaryString[0])
    return int(binaryString[0]) * 2 ** (len(binaryString) - 1) \
           + binaryToDecimal(binaryString[1:])

if __name__ == '__main__':
    print(binaryToDecimal('1100'))
