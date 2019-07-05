from tkinter import *

states = []                            # 改变对象，而非名称


def onPress(i):                       # 保存状态跟踪记录
    states[i] = not states[i]          # 由False变True, 由True变False

root = Tk()
for i in range(10):
    chk = Checkbutton(root, text=str(i), command=(lambda i=i: onPress(i)))
    chk.pack(side=LEFT)
    states.append(False)

root.mainloop()
print(states)
