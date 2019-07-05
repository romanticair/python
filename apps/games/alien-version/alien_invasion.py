import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# pygame.mixer模块可添加音效


def run_game():
    pygame.init()                                            # 初始化游戏并创建一个屏幕对象
    ai_settings = Settings()                                 # 配置信息类
    # 创建指定大小的游戏窗口, screen是一个surface, 游戏中每个元素都是一个surface
    # 激活动画循环后，每次循环都重绘这些surface
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    play_button = Button(screen, 'Play')                     # 创建Play按钮
    stats = GameStats(ai_settings)                           # 创建一个用于存储游戏统计信息的实例
    sb = Scoreboard(ai_settings, screen, stats)              # 分数等级等信息记录类
    # 创建一艘飞船、一个子弹编组、一个外星人编组
    # Group类似列表, 但其提供额外功能, 便于管理各个精灵
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)       # 创建一个外星人群
    # 开始游戏主循环
    while True:
        # 监听键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:                                # 游戏已开始?
            # 每次都更新飞船的位置(即使没有变)
            ship.update()
            # 每次都更新子弹的位置和已消失的子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # 每次都更新外星人的位置和其状态
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        # 用更新后的位置等信息绘制新屏幕(游戏结束也要执行)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
