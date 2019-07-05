from tkinter import *

# 极简主义/怀旧版
# 在内部def以**name参数形式来收集
Label(None, {'text': 'Hello GUI world', Pack: {'side': 'top'}}).mainloop()
# 可改成
# options = {'text': 'Hello GUI world'}
# layout = {'side': 'top'}
# Label(None, **options).pack(**layout)
