"""模拟随机漫步"""

from random import choice


class RandomWalk:
    """一个生产随机漫步数据的类"""
    def __init__(self, num_points=5000):            # 默认5000个点的随机漫步
        """初始化随机漫步的属性"""
        self.num_points = num_points
        self.x_values = [0]                         # 所有随机漫步都始于(0, 0)
        self.y_values = [0]

    def fill_walk(self):
        """计算随机漫步包含的所有点"""
        # 直到漫步包含所需点的数量
        while len(self.x_values) < self.num_points:
            x_step = self.get_step()                # 获取x的方向和距离
            y_step = self.get_step()                # 获取y的方向和距离
            if x_step == 0 and y_step == 0:        # 拒绝原地踏步
                continue
            next_x = self.x_values[-1] + x_step     # 计算下一个点的x和y值
            next_y = self.y_values[-1] + y_step     # 接着上一点所在的地方
            self.x_values.append(next_x)
            self.y_values.append(next_y)

    def get_step(self):
        """获取每次漫步的距离和方向"""
        # 决定去向以及沿该方向走的距离
        direction = choice([1, -1])               # 左还是右/上还是下?
        distance = choice([0, 1, 2, 3, 4])        # 走多远?
        step = direction * distance               # 计算出这一步
        return step



