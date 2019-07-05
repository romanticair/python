"""
公用超类：用于开启/关闭追踪消息
"""


class MailTool:                    # 所有邮件工具的超类
    def trace(self, message):       # 重新定义来禁用或者向文件输出日志
        print(message)


class SilentMailTool:             # 混合而非子类化
    def trace(self, message):
        pass
