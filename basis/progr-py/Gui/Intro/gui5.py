from tkinter import *


class HelloButton(Button):
    def __init__(self, parent=None, **config):  # 添加回调方法
        Button.__init__(self, parent, **config)  # 把自己打包起来
        self.pack()                              # 也可以设置样式
        self.config(command=self.callback)

    def callback(self):                        # 默认为按下动作
        print('Goodbye world...')                # 在子类中替换
        self.quit()

if __name__ == '__main__':
    HelloButton(text='Hello subclass world.').mainloop()
