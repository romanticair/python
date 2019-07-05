# 图形用户界面读取器端：将生成的程序标准输出传送到一个图形界面窗口

from Gui.Tools.guiStreams import redirectedGuiShellCmd     # 使用GuiOutput

redirectedGuiShellCmd('python -u pipe_nongui.py')            # -u 不缓存
