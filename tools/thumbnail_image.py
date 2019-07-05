import os
import sys
from PIL import Image

ext_list = ['.jpg', '.png', 'bmp']


def make_thumbnail(route, exts, size=(100, 100), to_gray=False):
    """
    缩略化文件路径指定后缀名的图片文件,如路径下有thumbnails文件夹，则可能会
    冲刷掉里面的文件。

    :param route: 文件路径
    :param exts: 扩展名
    :param size: pixel x pixel
    :param to_gray: 灰化
    :return: none
    """
    image_files = []
    os.chdir(route)
    for file_name in os.listdir('./'):
        if os.path.isfile(file_name) and os.path.splitext(file_name)[-1] in exts:
            image_files.append(file_name)

    if len(image_files) > 0:
        if not os.path.exists('thumbnails'):
            os.mkdir('thumbnails')
    else:
        print('there is no image in the level 1 of {0} directory.'.format(route))
        sys.exit(-1)

    index = 0
    for file in image_files:
        image = Image.open(file)
        image.thumbnail(size, Image.ANTIALIAS)    # 缩略化
        if to_gray:
            image = image.convert('L')            # 灰化
        index += 1
        image.save('thumbnails/' + '{:02}.jpg'.format(index))
    print('{0} image files were successfully made thumbnail.'.format(index))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[route][exts] needed, options [size][to_gray]')
    elif len(sys.argv) > 5:
        size = (int(sys.argv[3]), int(sys.argv[4]))
        make_thumbnail(sys.argv[1], sys.argv[2], size, sys.argv[5])
    elif len(sys.argv) > 4:
        size = (int(sys.argv[3]), int(sys.argv[4]))
        make_thumbnail(sys.argv[1], sys.argv[2], size)
    else:
        make_thumbnail(sys.argv[1], sys.argv[2])
