import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """相应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:            # 按键被按下?
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets, aliens)
        elif event.type == pygame.KEYUP:              # 按键被松开?
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:    # 鼠标按下?
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    # 该方法检测鼠标单击位置是否在Play矩形rect内并且要求游戏没有开始的状态
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """单击Play按钮后开始游戏的一些设置"""
    ai_settings.initialize_dynamic_settings()          # 重置游戏设置
    pygame.mouse.set_visible(False)                   # 隐藏光标(以免影响体验)
    stats.reset_stats()                                # 重置游戏统计信息
    stats.game_active = True                          # 激动游戏开始标志
    sb.prep_images()                                   # 更新得分、最高分、等级、剩余飞船数
    aliens.empty()                                     # 清空外星人和子弹列表
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)    # 创建一群新的外星人, 并让飞船居中
    ship.center_ship()


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets, aliens):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True                # 向右移动飞船
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True                 # 向左移动飞船
    elif event.key == pygame.K_SPACE:           # 按下的是空格
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:               # q 键退出
        sys.exit()
    elif not stats.game_active and event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False               # 取消向右移动飞船
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False                # 取消向左移动飞船


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没达到限制，就发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:     # 子弹数量没超过配置值则创建一颗子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)                        # 并将其加到编组bullets, 以便更新重绘


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 因为每次循环都绘制一个空屏幕, 先用背景色填充屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人前面重绘所有子弹
    for bullet in bullets.sprites():    # 该方法返回一个包含所有精灵的列表
        bullet.draw_bullet()             # 每个精灵都重绘
    ship.blitme()                        # 绘制飞船
    aliens.draw(screen)                  # 绘制编组中每个外星人
    sb.show_score()                      # 显示得分
    if not stats.game_active:           # 如果游戏处于非活动状态, 就绘制Play按钮
        play_button.draw_button()
    pygame.display.flip()                # 让绘制的屏幕可见, 所以要擦去旧屏幕(避免被覆盖)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置(编组update方法将自动对其中的每个精灵都调用update())
    bullets.update()
    for bullet in bullets.copy():       # 删除已消失的子弹(根据y值)
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人, groupcollide 检查碰撞(rect是否重叠)
    # 如果重叠，返回对应的字典(会有key-value)
    # 如果有，就自动删除相应的子弹和外星人，两实参True表示删除重叠的两个精灵
    # 如果要模拟子弹能穿杀外星人，则传入第一个布尔为 False
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:                                    # 击中一个外星人则加分
        for aliens in collisions.values():           # 这种方式包含同一颗子弹击倒多个外星人的数目, 不会遗漏
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)                   # 检查突破记录没有
    if len(aliens) == 0:                              # 开始新的一局
        start_new_level(ai_settings, stats, screen, sb, ship, aliens, bullets)


def start_new_level(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """打完了一波, 重整配置, 继续下一波"""
    bullets.empty()                     # 删除所有子弹, 加快游戏节奏, 并新建一群外星人
    ai_settings.increase_speed()
    stats.level += 1                    # 提高等级(打完一波)
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width  # 屏幕大小减去两倍外星人宽
    number_aliens_x = int(available_space_x / (2 * alien_width))    # 可容纳空间除去两倍外星人宽
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))       # 可容纳空间除去两倍外星人高
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    # 同一行间的每个外星人向右推移一个外星人的宽度
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # 不同行间的外星人向下推移一个外星人的高度
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人(外星人间距为外星人宽度)
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):                # 创建外星人群
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)   # 出现到达边缘就整体下移
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed      # 下移
    ai_settings.fleet_direction *= -1                     # 左右自动改变方向


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，也检查外星人和飞船有无碰撞的情况
    并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)                # 检查所有外星人
    aliens.update()                                       # 更新状态
    # 检测外星人和飞船间的碰撞(无碰撞返回None), 给定一个精灵和一编组
    # 检查是否有成员重叠, 遍历编组aliens，返回找到第一个碰撞的外星人
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1            # 将 ships_left 减1
        sb.prep_ships()                  # 更新记分牌
        aliens.empty()                   # 清空外星人列表和子弹列表
        bullets.empty()                  # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)                       # 暂停一下，让玩家知道被击到了
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  # 结束时显示光标


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.prep_high_score()
