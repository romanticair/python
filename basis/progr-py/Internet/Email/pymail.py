"""
pymail ---- 一个简单的Python命令行电子邮件接口客户端，使用Python的poplib模块查看POP
电子邮件信息，使用smtplib发送新邮件，使用email包提取邮件题头和负载及撰写邮件
"""

import poplib
import smtplib
import email.utils
from email.parser import Parser
from email.message import Message
# import mailconfig
import Internet.Email.mailconfig as mailconfig


helptext = """
Available commands:
i    - index display
l n? - list all messages (or just message n)
d n? - mark all messages for deletion (or just message n)
s n? - save all messages to a file (or just message n)
m    - compose and send a new mail message
q    - quit pymail
?    - display this help text
"""

fetchEncoding = mailconfig.fetchEncoding


def decode_to_unicode(messageBytes, fetchEncoding=fetchEncoding):
    """
    Py3.1:
    将抓取来的bytes类型解码成str类型Unicode字符串，以便显示或解析，使用全局设置（或
    操作平台特异的默认设置，题头检查，只能推测），在Python 3.2/3.2可能不需要这步：
    这种情况下信息不作变化，自己返回
    """
    return [line.encode(fetchEncoding) for line in messageBytes]


def splitaddrs(field):
    """
    在逗号后分割地址列表，允许姓名部分中存在逗号
    """
    pairs = email.utils.getaddresses([field])                         # [(姓名,地址)]
    return [email.utils.formataddr(pair) for pair in pairs]         # [(姓名,地址)]


def inputmessage():
    import sys
    From = input('From? ').strip()
    To = input('To? ').strip()                        # 题头的时间日期可以自动设置
    To = splitaddrs(To)                               # 可能有多个地址，可以用姓名+<地址>的格式
    Subj = input('Subj? ').strip()                    # 不要遇到','或者';'就分隔
    print('Type message text, end with line="."')
    text = ''
    while True:
        line = sys.stdin.readline()
        if line == '.\n':
            break
        text += line
    return From, To, Subj, text


def sendmessage():
    From, To, Subj, text = inputmessage()
    msg = Message()
    msg['From'] = From
    msg['To'] = ','.join(To)                                 # 对题头而非发送内容进行合并
    msg['Subject'] = Subj
    msg['Date'] = email.utils.formatdate()                   # 当前时间：rfc2822
    msg.set_payload(text)
    server = smtplib.SMTP(mailconfig.smtpservername)
    try:
        failed = server.sendmail(From, To, str(msg))         # 也可能抛出异常
    except:
        print('Error - send failed')
    else:
        if failed:
            print('Failed:', failed)


def connect(servername, user, passwd):
    print('Connecting...')
    server = poplib.POP3(servername)
    server.user(user)                           # 连接，登入邮件服务器
    server.pass_(passwd)                        # pass 是 Python的保留字
    print(server.getwelcome())                  # 打印返回的欢迎信息
    return server


def loadmessage(servername, user, passwd, loadfrom=1):
    server = connect(servername, user, passwd)
    try:
        print(server.list())
        msgCount, msgBytes = server.stat()
        print('There are', msgCount, 'mail messages in', msgBytes, 'bytes')
        print('Retrieving...')
        msgList = []                                       # 开始抓取邮件
        for i in range(loadfrom, msgCount + 1):           # 如果low >= high则内容为空
            hdr, message, octets = server.retr(i)          # 将文本存放到列表
            message = decode_to_unicode(message)           # bytes字符串转换成str字符串
            msgList.append('\n'.join(message))             # 将邮件留在服务器上
    finally:
        server.quit()
    assert len(msgList) == (msgCount - loadfrom) + 1      # msg编号从1开始
    return msgList


def deletemessages(servername, user, passwd, toDelete, verify=True):
    print('To be deleted:', toDelete)
    if verify and input('Delete?')[:1] not in ('y', 'Y'):
        print('Delete cancelled.')
    else:
        server = connect(servername, user, passwd)
        try:
            print('Deleting messages from server...')
            for msgnum in toDelete:                        # 重新连接，删除邮件
                server.dele(msgnum)                         # 邮箱在quit()之前一直处于锁定状态
        finally:
            server.quit()


def showindex(msgList):
    count = 0                                                    # 显示部分邮件题头
    for msgtext in msgList:
        msghdrs = Parser().parsestr(msgtext, headersonly=True)  # 在3.1中应为str
        count += 1
        print('%d:\t%d bytes' % (count, len(msgtext)))
        for hdr in ['From', 'To', 'Date', 'Subject']:
            try:
                print('\t%-8s=>%s' % (hdr, msghdrs[hdr]))
            except KeyError:
                print('\t%-8s=>%s (unkown)' % hdr)
        if count % 5 == 0:
            input('[Press Enter Key]')                           # 每5个输入后暂停一次


def showmessage(i, msgList):
    if 1 <= i <= len(msgList):
        # print(msgList[i-1])                           # 老方法：打印整个邮件 ---- 题头+文本
        print('-' * 80)
        msg = Parser().parsestr(msgList[i-1])           # 在3.1中应为str
        content = msg.get_payload()                     # 打印负载：字符串，或[消息]
        if isinstance(content, str):                    # 只保留末尾的行尾符
            content = content.rstrip() + '\n'
        print(content)
        print('-' * 80)                                 # 为了只获取文本，请参考email.parsers
    else:
        print('Bad message number')


def savemessage(i, mailfile, msgList):
    if 1 <= i <= len(msgList):
        savefile = open(mailfile, 'a', encoding=mailconfig.fetchEncoding)
        savefile.write('\n' + msgList[i-1] + '-'*80 + '\n')
    else:
        print('Bad message number')


def msgnum(command):
    try:
        return int(command.split[1])
    except:
        return -1                                                 # 假定失败


def interact(msgList, mailfile):
    showindex(msgList)
    toDelete = []
    while True:
        try:
            command = input('[Pymail] Action? (i, l, d, s, m, q, ?)')
        except EOFError:
            command = 'q'
        if not command:
            command = '*'
        if command == 'q':                                        # 退出
            break
        elif command[0] == 'i':                                   # 索引
            showindex(msgList)
        elif command[0] == 'l':                                   # 列表
            if len(command) == 1:
                for i in range(1, len(msgList) + 1):
                    showmessage(i, msgList)
            else:
                showmessage(msgnum(command), msgList)
        elif command[0] == 's':                                   # 保存
            if len(command) == 1:
                for i in range(1, len(msgList) + 1):
                    savemessage(i, mailfile, msgList)
            else:
                savemessage(msgnum(command), mailfile, msgList)
        elif command[0] == 'd':                                   # 删除
            if len(command) == 1:                                  # 稍后删除所有邮件
                toDelete = list(range(1, len(msgList) + 1))        # 3.x要求列表
            else:
                delnum = msgnum(command)
                if (i <= delnum <= len(msgList)) and (delnum not in toDelete):
                    toDelete.append(delnum)
                else:
                    print('Bad message number')
        elif command[0] == 'm':                                   # 邮件
            sendmessage()                                          # 通过SMTP发送新邮件
            # execfile('smtpmail.py', {})                          # 或者：在各自的命名空间里运行各文件
        elif command[0] == '?':
            print(helptext)
        else:
            print('What? -- type "?" for commands help')
    return toDelete


if __name__ == '__main__':
    import getpass
    mailserver = mailconfig.popservername                           # 如: 'pop.qq.com'
    mailuser = mailconfig.popusername                               # 如: 'user_bigsir@163.com'
    mailfile = mailconfig.savemailfile                              # 如: L:\Test\savemail
    mailpassswd = getpass.getpass('Password for %s?' % mailserver)  # 邮箱密码
    print('[Pymail email client]')
    msgList = loadmessage(mailserver, mailuser, mailpassswd)        # 全部载入
    toDelete = interact(msgList, mailfile)
    if toDelete:
        deletemessages(mailserver, mailuser, mailpassswd, toDelete)
    print('Bye.')
