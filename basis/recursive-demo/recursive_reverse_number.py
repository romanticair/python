
def reverseDisplay(value):
    if value < 10:
        return value
    print(value % 10, end="")
    return reverseDisplay(value // 10)

if __name__ == '__main__':
    print(reverseDisplay(12345))