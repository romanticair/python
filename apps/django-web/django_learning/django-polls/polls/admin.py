from django.contrib import admin

from .models import Question, Choice
# Register your models here.


class ChoiceInline(admin.TabularInline):            # 下面的方法占用了大量区域
    model = Choice                                     # 这里提供了单行显示关联对象的方法
    extra = 3

# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3                                               # 管理的选项插槽在这里定义


class QuestionAdmin(admin.ModelAdmin):                     # 模型后台类(字段顺序是列表是顺序)
    # fields = ['pub_date', 'question_text']
    fieldsets = [                                             # 当拥有多个字段的表单时,
        (None,              {'fields': ['question_text']}),  # 将它们分为几个字段集
        ('Date information', {'fields': ['pub_date'], 'classes':
            ['collapse']}),                       # 元组首元素是字段集的标题
    ]                                             # 告诉Choice对象要在Question后台页面编辑
    inlines = [ChoiceInline]                      # 默认提供3个足够的选项字段
    list_display = ('question_text', 'pub_date',
                    'was_published_recently')     # 包含要显示的字段名的元组, 显示单个字段
    list_filter = ['pub_date']                    # 优化Qusetion变更页,看models.py的配置
    search_fields = ['question_text']             # 提供可搜索的字段

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
