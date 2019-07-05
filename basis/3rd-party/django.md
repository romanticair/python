## 一、Django基本命令
1. 新建一个项目
  `$ django-admin startproject project-name`

2. 新建app
  > 一个项目一般有多个 app

  `$ python manage.py startapp app-name1`
  `$ django-admin.py startapp app-name2`

3. 同步数据库
  `$ python manage.py migrate`
  > 创建数据库(将修改数据库称为迁移数据库)-迁移

  `$ python manage.py makemigrations app`
  > 模型有变化, 进行项目迁移,自动更新数据库信息
  > 注意: 创建数据库后,当新模型,需要再次迁移数据库,先执行 `makemigrations`, 生成一个新的迁移文件,然后再执行 migrate 应用该迁移

4. 使用开发服务器
  `$ python manage.py runserver`
  > 默认8000端口(不用指定)

  `$ python manage.py runserver port`
  > 当端口被占用，可指定其它端口(一般8000以上)

  `$ python manage.py runserver ip:port`
  > 监听所有可用ip(内外网)
  > 注意: 如果是在另一台电脑上访问要指定 0.0.0.0:8000，比如监听所有 ip 监听机器上所有8000端口，访问时用电脑的ip代替 127.0.0.1。

5. 清空数据库
  `$ python manage.py flush`
  > 只留下空表(超级用户啥的都清空了)

6. 创建超级管理员
  `$ python manage.py createsuperser`
  > 具备所有权限,管理(客户端访问权限等)

  `$ python manage.py changepassword username`
  > 修改用户密码，管理需要使用超级用户访问管理网站 localhost:8000/admin/。
  > 注意: Django自动在管理网站中添加了模型如User和Group，我们创建的模型必须人工进行注册(向管理网站(admin.site.register())注册模型)。

7. 导入/出数据
  `$ python manage.py dumpdate app-name > app-name.json`
  `$ python manage.py loaddate app-name.json`

8. 项目环境终端
  该环境可调用项目的models.py中的API(测试用)
  `$ python manage.py shell`

9. 数据库命令行
  进入 settings.py 设置的数据库(能够执行SQL语句)
  `$ python manage.py dbshell`

10. 更多命令
  `$ python manage.py`



## 二、目录结构与说明
```
1 mysite                       # 创建的项目
2 ├── manage.py
3 └── mysite
4     ├── __init__.py
5     ├── settings.py
6     ├── urls.py
7     └── wsgi.py
8 learn/                       # 创建的应用(app)
9     ├── __init__.py
10    ├── admin.py
11    ├── models.py
12    ├── tests.py
13    ├── views.py
14    ├── apps.py
14    └── templates/           # 模板文件夹
15        ├── learn/
16            ├── base.html
17            ├── index.html
18            └── *.*
```
+ 文件说明
1. 部署服务器, 网关接口文件 wsgi.py (Web Server Gateway Interface)
2. 地址路由配置文件(映射到视图) urls.py
3. 向管理网站注册模型 admin.py
4. 模型建立 models.py
5. 激活模型 settings.py

+ 创建应用程序
1. 定义模型 01
2. 激活模型(将 app 包含在项目中)
3. 注册模型
4. 定义模型 02
5. 迁移模型
6. 注册模型

+ 创建网页流程
1. 定义 URL
2. 编写视图 views
3. 编写模板 templates
> 每个url都被映射到视图----视图函数获取并处理页面所需数据(通常是调用一个模板(网页))
> 注意: urls.py文件、templates文件夹、learning_logs文件夹都是手动创建的, 其中learning_logs在templates里创建, templates在初创app文件夹里创建。



## MVC同步化操作
+ 模型(Model)，即数据存取层
+ 模板(Template)，即业务逻辑层
+ 视图(View)，即表现层

1. 新定义的 app 要在 settings.py 中的 INSTALL_APPS 数据结构中注册
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    # --skip--
    'django.contrib.staticfiles',
    # 在这注册我们的 app
    'learn',
)
```

> django 能够自动找到 app 中的模板文件(app-name/templates/下的文件)和静态文件(app-name/static/中的文件)



2. 视图函数(访问页面时的内容)
打开 learn/views.py
```python
# --skip--
def index(request):                   # 请求get, post, 数据库调用等反馈信息都在本文件进行
    return render(request, 'Hello！') # 像print一样, 但这里是把信息渲染到页面
```

3. 路由配置
打开 mysite/mysite/urls.py
```python
from django.conf.urls import url
from django.contrib import admin
from learn import views as learn_views  # new

urlpatterns = [
    url(r'^$', learn_views.index),        # new
    url(r'^admin/', admin.site.urls),     # 正则匹配 url
]
```



## Shell 命令

```
>>> themes = Class.objects.all()     # 获取模型实例(又称查询集)可遍历
>>> for theme in themes:
        print(theme.id, theme)       # 查看分配给主题对象的id以及字符串表示

1 Chess
2 Rock Clinmbing

>>> t = Class.objects.get(id=1)      # 通过id获取指定对象实例
>>> t.text                           # 可查看其属性
'Chess'

>>> t.entry_set.all()                # 定义了外键(如条目与主题关联), 则返回相对应的所有条目(类名小写+set/get)
--skip--                             # entry是模型Entry类的小写(Django自动处理的)

>>> Class.objects.order_by('-date_added')  # 按时间排序(在前面加'-')

>>> t.save()                         # 保存到数据库

# Django provides a rich database lookup API that's entirely driven by keyword arguments.
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>

>>> q = Question.objects.get(pk=1)
# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
<QuerySet []>

# Create three choices.
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>

>>> q.choice_set.count()
>>> q.delete()
```

> 注意：'__ '两个下划线可以理解为代表 python 中的'.'



## 模板继承
### 一、模板
1. 父模板 base.html
模板签名({% %})，该 URL 与 learning_logs/urls.py 中定义为 index 的 URL 模式匹配。
learning_logs 是一个命名空间(在 urls 中 app_name 写上,app 多了的时候能够区别 URL ), index 是该命名空间中一个独特的URL模式
`<a href="{% url 'learning_logs:index' %}">Learning Log<a/>`

一对块标签, 块名为 `content` --是一个占位符, 包含的信息由子模板指定
`{% block content %}{% endblock content %}`

2. 子模板 *.html
让Django知道它继承了哪个父模板(将导入父模板所有内容)

```html
{% extends "learning_logs/base.html" %}
定义 content 块(不是从父模板继承的内容都包含在 content 中)
{% block content %}
content 块结束的位置
{% endblock content %}
```

3. 其它标签
相当于 for 循环的模板标签(遍历字典 context 中的列表 topics)
```html
{% for topic in topics %}
必须用此标签结束循环
{% endfor %}
topic都被替换成topic的当前值(模板变量)
{{ topic }}
该标签告诉Django在列表topics为空时的情况
{% empty %}
```

> | 表示模板过滤器----对模板变量的值进行修改的函数
> 过滤器 linebreaks 将包含换行符的长条目转换为浏览器能够理解的格式

```html
<p>{{ entry.date_added|date:'M d, Y H:i' }}</p>
<p>{{ entry.text|linebreaks }}</p>
```
date:'M d, Y H:i' 以这样的格式显示时间戳: January 1, 2015 23:00

根据 learning_logs 中名为 topic 的 URL 模式来生成合适的链接，该URL模式要求提供实参 topic_id, 因此在模板标签url中添加属性 topic.id
`<a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>`



### 二、if 语句

```html
{% if error_message %}
  <p>{{ error_message }}</p>
{% endif %}
```



### 三、表单处理

```html
<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
        {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}"
               value="{{ choice.id }}"/>
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label>
        <br/>
    {% endfor %}
</form>
```

> 每个单选按钮的 value 属性对应的是各个 Choice 的 ID, 当有提交时,它将发送一个 POST 数据 choice=#,其中 `#` 为选择的 Choice 的ID, forloop.counter 指示 for 标签已循环了多少次。
> 注意: 所有针对内部 URL 的 POST 表单都应该使用 {% csrf_token %} 模板标签
