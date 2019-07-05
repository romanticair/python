"""
实现用来查看和更新保存在shelve中类实例的基于Web的界面；
shelve保存在服务器上(如果是本地机器的话，就是同一个机器)
"""

import cgi
import html
import shelve
import sys
import os

shelve_name = 'class-shelve'      # shelve文件在当前工作目录
field_names = ('name', 'age', 'job', 'pay')

form = cgi.FieldStorage()         # 解析表单数据
print('Content-type: text/html')  # 响应html
sys.path.insert(0, os.getcwd())   # 为了这个和pickler能查找person模块

# 主html模板
reply_html = """
<html>
<title>People Input Form</title>
<body>
<form method="post" action="people_cgi.py">
    <table>
        <tr><th>Key<td><input type="text" name="key" value="%(key)s">
        $ROWS$
    </table>
    <p>
    <input type="submit" value="Fetch", name="action">
    <input type="submit" value="Update", name="action">
</from>
</body>
</html>"""

# 为$ROWS$的数据行插入html
row_html = '<tr><th>%s<td><input type="text" name="%s" value="%%(%s)s">\n'
rows_html = ''
for field_name in field_names:
    rows_html += (row_html % ((field_name, ) * 3))
reply_html = reply_html.replace('$ROWS$', rows_html)


def htmlize(a_dict):
    new = a_dict.copy()
    for field in field_names:                 # 值可能包含特殊字符
        value = new[field]                     # 作为代码显示：被引号引起
        new[field] = html.escape(repr(value))  # 转义html字符
    return new


def fetch_record(db, form):
    try:
        key = form['key'].value
        record = db[key]
        fields = record.__dict__  # 使用属性字典
        fields['key'] = key       # 填充响应字符串
    except Exception:
        fields = dict.fromkeys(field_names, '?')
        fields['key'] = 'Missing or invalid key!'
    return fields


def update_record(db, form):
    if 'key' not in form:
        fields = dict.fromkeys(field_names, '?')
        fields['key'] = 'Missing key input!'
    else:
        key = form['key'].value
        if key in db:
            record = db[key]                    # 更新已有记录
        else:
            from person import Person         # 为键值创建/保存新记录
            record = Person(name='?', age='?')  # eval: 字符串必须被引号引起
        for field in field_names:
            setattr(record, field, eval(form[field].value))

        db[key] = record
        fields = record.__dict__
        fields['key'] = key
    return fields


db = shelve.open(shelve_name)
action = form['action'].value if 'action' in form else None
if action == 'Fetch':
    fields = fetch_record(db, form)
elif action == 'Update':
    fields = update_record(db, form)
else:
    fields = dict.fromkeys(field_names, '?')  # 错误的提交按钮值
    fields['key'] = 'Missing or invalid action!'

db.close()
print(reply_html % htmlize(fields))           # 使用dict来填充响应
