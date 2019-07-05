class Settings:
    """存储 <外星人入侵> 的所有设置"""
    def __init__(self):
        # 屏幕属性设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # 飞船属性设置(相当于游戏币)
        self.ship_limit = 2
        # 子弹属性设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # 外星人设置
        self.fleet_drop_speed = 10                   # 撞到边缘时下降的速度
        self.speedup_scale = 1.1                     # 以这样的速度递增方式加快游戏节奏
        self.score_scale = 1.5                       # 每一波外星人点数的提高速度

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右移，为-1表示向左移, 开始时外星人总是向右移动
        self.fleet_direction = 1
        # 初始点数(击倒外星人获得的点数)
        self.alien_points = 50

    def increase_speed(self):
        """提高速度和点数的设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
