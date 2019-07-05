"""
对图片，滤镜，模糊，缩放等
ImageDraw 还提供了一系列绘图方法, 可直接绘图, 如要生成字母验证码图片
"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 1.来看看最常见的图像缩放操作
# 打开一个 jpg 图像文件, 注意是当前路径
im = Image.open('KEBI.jpg')
# 获取图像尺寸
w, h = im.size
print('Original image sise: %sx%s' %(w, h))
# 缩放到50%
im.thumbnail((w//2, h//2))
print('Resize im to: %sx%s' %(w//2, h//2))
# 把缩放后的图像用jpeg格式保存
im.save('thumbnail.jpeg', 'jpeg')

# 2.模糊效果
im = Image.open('KEBI.jpg')
# 应用模糊滤镜
im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.jpeg', 'jpeg')


def rndChar():
    """随机字母"""
    return chr(random.randint(65, 90))

def rndColor1():
    """随机颜色1"""
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def rndColor2():
    """随机颜色2"""
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

# 240 x 60
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象
font = ImageFont.truetype('Fonts/arial.ttf', 36)
# 创建Draw对象
draw = ImageDraw.Draw(image)
# 填充每个像素
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill = rndColor1())

# 输出文字
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())

# 模糊
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
