import os

print('setevn...', end='')
print(os.environ['USERNAME'])      # 输出当前shell的变量值

os.environ['USERNAME'] = 'Brian'   # 在后台运行 os.putenv
os.system('python echoenv.py')

os.environ['USERNAME'] = 'Arthur'  # 传递更新值到衍生程序
os.system('python echoenv.py')     # 链接的C语言库模块

os.environ['USERNAME'] = input('?')
print(os.popen('python echoenv.py').read())
