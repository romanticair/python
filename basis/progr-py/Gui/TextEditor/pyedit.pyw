#!/usr/bin/python
"""
便利的脚本从任意地点按要求导入路径设置来启动 pyedit, sys.path 用来导入， open()函数必须
对应已知顶层脚本的目录，而不是cwd ---- 如果通过快捷方式或图标点击的方式运行，那么cwd是脚
本的目录，但有可能是任何东西，条件是从命令行输入到一个有框的控制台窗口来运行: 使用argv路径，
这是一个.pyw来压制Windows系统上控制台弹出；增加这些脚本的目录至你的系统路径来从命令行运行；
此方法也适用于Unix系统: 可灵活处理/和\。
"""

import sys
import os

mydir = os.path.dirname(sys.argv[0])                     # 使用我的目录来打开路径
sys.path.insert(1, os.sep.join([mydir] + ['..'] * 3))    # 进入: ProgrammingPython根目录, 上3级目录
exec(open(os.path.join(mydir, 'textEditor.py')).read())
