from django.contrib import admin

# Register your models here.


from learning_logs.models import Topic, Entry


# 向管理网站注册Topic和Entry
admin.site.register(Topic)
admin.site.register(Entry)
