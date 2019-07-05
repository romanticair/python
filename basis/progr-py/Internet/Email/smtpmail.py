"""
使用Python的SMTP邮件接口模块发送电子邮件消息，这个脚本值是一个单词运行的简单发送脚本
请参考pymail，PyMailGUI和PyMailCGI等带有更多用户交互特性的客户端，还可以参考用于收取
邮件的脚本popmail.py，处理附件及利用标准库email包进行格式化的mailtools包。
"""

import sys
import smtplib
import mailconfig
import email.utils

mailserver = mailconfig.smtpservername

From = input('From?').strip()                   # 或者从mailconfig导入
To = input('To?').strip()                       # 比如: python-list@python.org
Tos = To.split(';')                             # 允许收件人组成的列表
Subj = input('Subj?').strip()
Date = email.utils.formatdate()                 # 当前日期时间，rfc2822

# 标准题头，后面是空行，然后是文本
text = ('Form: %s\nTo: %s\nDate: %s\nSubject: %s\n\n' % (From, Tos, Date, Subj))
print('Type message text, end with line=[Ctrl+d (Unix), Ctrl+z (Windows)]')
while True:
    line = sys.stdin.readline()
    if not line:
        break                                   # 输入ctrl-d/z时退出
    # if line[:4] == 'From':
    #     line = '>' + line                      # 服务器可能进行了转义
    text += line

print('Connecting...')
server = smtplib.SMTP(mailserver)                # 连接，没有登录步骤
failed = server.sendmail(From, Tos, text)
server.quit()
if failed:                                       # smtplib也可能抛出异常
    print('Failed recipients:', failed)          # 不过这里先让它们通过
else:
    print('No errors.')
print('Bye.')
