"""read numbers till eof and show squares"""


def interact():
    print('Hello stream world')               # 输出数据到sys.stdout
    while True:
        try:
            reply = input('Enter a number>')  # 输入来自sys.stdin的数据
        except EOFError:
            break                            # 在结尾处抛出一个异常
        else:
            num = int(reply)
            print('%d squared is %d' % (num, num ** 2))
    print('Bye')

if __name__ == '__main__':
    # Dos: python teststreams.py < input.txt ?
    # Dos: python teststreams.py < input.txt > out.txt ?
    interact()