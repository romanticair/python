from django.db import models
from django.contrib.auth.models import User

"""在代码城层模型就是类"""

# Create your models here.
# Django的Model是一个定义了模型基本功能的类


class Topic(models.Model):
    """用户学习的主题(仅有两个属性text, date_added)"""
    text = models.CharField(max_length=200)                # 文本组成(200字符)
    date_added = models.DateTimeField(auto_now_add=True)  # 自动记录日期时间
    owner = models.ForeignKey(User, on_delete=True)       # 添加关联后,特定条目与特定主题相关联

    def __str__(self):
        return self.text                                  # 默认使用该属性显示有关主题的信息


class Entry(models.Model):
    """学到有关某个主题的具体知识(为添加的条目定义本模型(多对一))"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # 外键(将每个条目关联到主题)
    text = models.TextField()                                   # 不限制条目长度的text
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:                        # 存储用于管理模型的额外信息(能够设置一个特殊属性)
        verbose_name_plural = 'entries'  # 需要时,可用其表示多个条目(否则Django将使用Entrys表示)

    def __str__(self):
        """返回模型的字符串表示"""
        text = self.text[:50]
        return text + '...' if len(text) > 50 else text
