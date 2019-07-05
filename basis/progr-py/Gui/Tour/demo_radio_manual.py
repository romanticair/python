"""
单选按钮，困难的方法(不使用变量)
请注意，取消单选按钮仅仅意味着
设置其按钮的关联账值为空字符串，所以我们仍需要
赋予按钮特殊值，或改为使用多选按钮；
"""
from tkinter import *

state = ''
buttons = []


def onPress(i):
    global state
    state = i
    for btn in buttons:
        btn.deselect()

    buttons[i].select()

root = Tk()
for i in range(10):
    rad = Radiobutton(root, text=str(i), value=str(i), command=(lambda i=i: onPress(i)))
    rad.pack(side=LEFT)
    buttons.append(rad)

onPress(0)  # 选择初始化
root.mainloop()
print(state)
