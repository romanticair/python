"""
使用Python POP3邮件接口模块查看你的POP电子邮件账户的消息，这只是一个劲简单的目录获
取 ---- 请参考带有更多互动特性的客户端pymail.py，以及用于邮件发送的smtpmail.py脚本；
POP用于邮件获取，运行在服务器机器上使用端口110的套接字上，不过Python的poplib隐藏了
所有协议细节，想要发送邮件，可以使用smtplib模块（或os.popen('mail...')）。另请参考
作为IMAP替代方案的imaplib模块，以及PyMailGUI/PyMailCGI里的更多特性；
"""

import sys
import poplib
import getpass
import mailconfig

mailserver = mailconfig.popservername           # 例如: 'pop.rmi.net'
mailuser = mailconfig.popusername               # 例如: 'lutz'
mailpasswd = getpass.getpass('Password for %s?' % mailserver)

print('connecting...')
# server = poplib.POP3(mailserver)
server = poplib.POP3_SSL(mailserver)            # 我这个账号设置了第三方必须SSL
server.user(mailuser)                           # 连接，登录邮件服务器
server.pass_(mailpasswd)                        # pass是Python的保留字

try:
    print(server.getwelcome())                  # 打印所返回的欢迎信息
    msgCount, msgBytes = server.stat()
    print('There are', msgCount, 'mail messages in', msgBytes, 'btyes')
    print(server.list())
    print('-' * 80)
    input('[Press Enter key]')
    for i in range(msgCount):
        hdr, message, octets = server.retr(i+1)  # octets是字节数,迭代抓取邮箱里的第i封邮件
        for line in message:
            print(line.encode())                 # 抓取，打印所有邮件
            print('-' * 80)                      # 邮件文本在3.x是字节
            if i < msgCount - 1:
                input('[Press Enter key]')       # 邮件在quit前翼子处于锁定状态
finally:                                        # 确保解锁了邮箱
    server.quit()                                # 否则一直锁定到连接超时
print('Bye.')


