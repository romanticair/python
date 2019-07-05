from tkinter import *

# 创建后再设置
widget = Label()
# 指定文本关键字，加载的组件对象(拦截)对操作做索引
# 因此选项可用来做映射键
widget['text'] = 'Hello GUI world!'
widget.pack(side=TOP)
mainloop()
