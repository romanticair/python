class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, ai_setting):
        """初始化统计信息"""
        self.ai_settings = ai_setting
        self.reset_stats()
        self.game_active = False   # 让游戏一开始时处于非活动状态
        self.high_score = 10000     # 在任何情况下都不应重置最高得分(考虑将该数据持久化?)

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

