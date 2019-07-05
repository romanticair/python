"""
不利己启动所有小工具，仅允许PyGardgets工具栏；
使用pyw文件可避免在Windows下的DOS弹窗，将后缀改为 ".py"，即可查看控制台消息
"""
import PyGadgets
PyGadgets.runLauncher(PyGadgets.mytools)