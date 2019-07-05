import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings                        # 配置信息类
        self.image = pygame.image.load('images\ship.bmp')     # 加载飞船图像并获取其外接矩形
        self.rect = self.image.get_rect()                     # 获取 surface(image) 的属性 rect
        self.screen_rect = screen.get_rect()
        # 通过将屏幕的坐标和方位元素赋值给要绘制的矩形位置
        # 这里是将一艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx          # 屏幕中心x轴
        self.rect.bottom = self.screen_rect.bottom            # 屏幕底部y轴
        self.center = float(self.rect.centerx)                # 在飞船的属性 center 中存储小数值
        self.moving_right = False                            # 两个移动方向的标志
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船的center值, 而不是rect, 因为矩形只能存储值的整数部分，速度控制不够灵活
        if self.moving_right and self.rect.right < self.screen_rect.right:   # 移动方向 + 边界检查
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:                          # 移动方向 + 边界检查
            self.center -= self.ai_settings.ship_speed_factor
        # 根据 self.center 更新 rect 对象, 这里也是只存储整数部分
        self.rect.centerx = self.center

    def blitme(self):
        """在屏幕上绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
