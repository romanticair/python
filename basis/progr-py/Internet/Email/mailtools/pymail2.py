"""
pymail2 ---- Python实现的简单的控制台电子邮件接口客户端，这一版使用了mailtools包，而
后者使用了poplib，smtplib和email包来解析和撰写电子邮件；显示邮件的首个文本部分而非全文；
初始抓取使用TOP命令，仅抓取邮件题头，仅抓取选中的待显示邮件的全文；缓存已抓取的邮件；
缺陷：没有索引刷新方法；使用独立的mailtools对象 ---- 后者也可以用作超类;
"""
from Internet.Email import mailtools
from Internet.Email.pymail import inputmessage
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
mailcache = {}


def fetchmessage(i):
    try:
        fulltext = mailcache[i]
    except KeyError:
        fulltext = fetcher.downloadMessage(i)
    return fulltext


def sendmessage():
    From, To, Subj, text = inputmessage()
    sender.sendMessage(From, To, Subj, [], text, attaches=None)


def deletemessages(toDelete, verify=True):
    print('To be deleted:', toDelete)
    if verify and input('Delete?')[:1] not in ('y', 'Y'):
        print('Delete cancelled.')
    else:
        print('Deleting messages from server...')
        fetcher.deleteMessages(toDelete)


def showindex(msgList, msgSizes, chunk=5):
    count = 0
    for (msg, size) in zip(msgList, msgSizes):                  # email.message.Message, 整形
        count += 1                                               # 这里运行3.x迭代没问题
        print('%d:\t%d bytes' % (count, size))
        for hdr in ['From', 'To', 'Date', 'Subject']:
            print('\t%-8s=>%s' % (hdr, msg.get(hdr, '(unkown)')))
        if count % chunk == 0:
            input('[Press Enter Key]')                           # 每chunk个输入后暂停一次


def showmessage(i, msgList):
    if 1 <= i <= len(msgList):
        fulltext = fetchmessage(i)
        message = parser.parseMessage(fulltext)
        ctype, maintext = parser.findMainText(message)
        print('-' * 79)
        print(maintext.rstrip() + '\n')                 # 主题文本部分，而非整封邮件
        print('-' * 70)                                 # 也不是其后的附件
    else:
        print('Bad message number')


def savemessage(i, mailfile, msgList):
    if 1 <= i <= len(msgList):
        fulltext = fetchmessage(i)
        savefile = open(mailfile, 'a', encoding=mailconfig.fetchEncoding)
        savefile.write('\n' + fulltext + '-'*80 + '\n')
    else:
        print('Bad message number')


def msgnum(command):
    try:
        return int(command.split()[1])
    except:
        return -1  # 假定这么做失败了


def interact(msgList, msgSizes, mailfile):
    showindex(msgList, msgSizes)
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
            showindex(msgList, msgSizes)
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
                if (1 <= delnum <= len(msgList)) and (delnum not in toDelete):
                    toDelete.append(delnum)
                else:
                    print('Bad message number')
        elif command[0] == 'm':                                   # 邮件
            sendmessage()                                          # 通过SMTP发送新邮件
        elif command[0] == '?':
            print(helptext)
        else:
            print('What? -- type "?" for commands help')
    return toDelete


def main():
    global parser, sender, fetcher
    mailserver = mailconfig.popservername
    mailuser = mailconfig.popusername
    mailfile = mailconfig.savemailfile

    parser = mailtools.MailParser()
    sender = mailtools.MailSender()
    fetcher = mailtools.MailFetcherConsole(mailserver, mailuser)

    def progress(i, max):
        print(i, 'of', max)

    hdrsList, msgSizes, ignore = fetcher.downloadAllHeaders(progress)
    msgList = [parser.parseHeaders(hdrtext) for hdrtext in hdrsList]
    print('[Pymail email client]')
    toDelete = interact(msgList, msgSizes, mailfile)
    if toDelete:
        deletemessages(toDelete)

if __name__ == '__main__':
    main()
