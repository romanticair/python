"""
ps: 这是要自己建立的文件, 定义learning_logs的URL模式
功能: 将URL映射到views"""

from django.conf.urls import url
from django.urls import re_path

from . import views

app_name = 'learning_logs'
# 包含了可在learning_logs应用程序中请求的所有页面(正在匹配url, 调用视图函数
urlpatterns = [  # 最后一个参数, 能够让我们在其它地方引用它(如需要提供该主页登录链接, 而不是写URL)
    # 主页 /learning_logs/
    url('^$', views.index, name='index'),
    # 主题 /learning_logs/topics/
    url(r'^topics/$', views.topics, name='topics'),
    # 特定主题的详细页面((?P<topic_id>\d+)将捕获任何数值赋值给实参topic_id)
    # url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # 详细页面/learning_logs/topics/1/   topic_id实参将被传递给topic函数处理
    re_path('topics/(?P<topic_id>\d+)/', views.topic, name='topic'),
    # 用于添加新主题的网页
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 用于添加新条目的页面
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # 用于编辑条目的页面
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
