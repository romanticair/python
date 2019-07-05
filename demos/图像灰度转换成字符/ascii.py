import argparse
from PIL import Image


def transform():
    img = Image.open(IMG)
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)
    txt = ''
    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*img.getpixel((j, i)))
        txt += '\n'

    print(txt)
    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open('output.txt', 'w') as f:
            f.write(txt)


def get_char(r, g, b, alpha=256):
    # 将 256灰度 映射到70个字符串上
    if alpha == 0:
        return ' '

    length = len(ascii_char)
    # 灰度值公式将像素的 RGB 值映射到灰度值
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    # value = int((gray/unit))
    # return ascii_char[int((gray/unit))] if value < 60 else ' '
    return ascii_char[int((gray/unit))]

	
if __name__ == '__main__':
    # 命令行输入参数处理
    parser = argparse.ArgumentParser()
    # 输入文件
    parser.add_argument('file')
    # 输出文件
    parser.add_argument('-o', '--output')
    # 输出字符画宽
    parser.add_argument('--width', type=int, default=80)
    # 输出字符画高
    parser.add_argument('--height', type=int, default=80)
    # 获取参数
    args = parser.parse_args()

    IMG = args.file
    WIDTH = args.width
    HEIGHT = args.height
    OUTPUT = args.output
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    transform()
