"""
提取、删除，匹配POP服务器中的邮件
"""
import sys
import poplib
import Internet.Email.mailconfig as mailconfig
from .mailParser import MailParser                  # 为进行题头匹配
from .mailTool import MailTool, SilentMailTool      # 追踪控制超类

print('user:', mailconfig.popusername)

# 索引/服务器消息编号不同步时的测试
class DeleteSynchError(Exception):pass            # 删除时信息不同步
class TopNotSupported(Exception):pass             # 不能允许同步化测试
class MessageSynchError(Exception):pass           # 索引列表不同步


class MailFetcher(MailTool):
    """
    抓取邮件：链接，抓取题头和邮件，删除邮件；
    可在任何带有Python和互联网的机器上运行，子类化以实现缓存；
    用POP协议实现，IMAP要求新类；
    抓取时为解析器进行全部邮件文本的解码。
    """
    def __init__(self, popserver=None, popuser=None, poppswd=None, hastop=True):
        self.popServer = popserver or mailconfig.popservername
        self.popUser = popuser or mailconfig.popusername
        self.srvrHasTop = hastop
        self.popPassword = poppswd                   # 如果None则稍后询问

    def connect(self):
        self.trace('Connecting...')
        self.getPassword()                           # 文件，GUI或控制台
        server = poplib.POP3_SSL(self.popServer)
        # server = poplib.POP3(self.popServer)
        server.user(self.popUser)                    # 连接，登录POP服务器
        server.pass_(self.popPassword)               # pass是Python的保留字
        self.trace(server.getwelcome())              # 打印返回的欢迎信息
        return server

    # 可在类或实例中修改以进行定制
    fetchEncoding = mailconfig.fetchEncoding

    def decodeFulltext(self, messageBytes):
        """
        将抓取到的全部邮件文本字节解码成str Unicode字符；抓取时完成，以备后续
        的显示或解析(此后完整邮件文本一直是Unicode)；用类特异或实例特异的设置
        或常用类型进行解码，还可以尝试题头检查，或者根据结构进行智能推测；在Python
        3.2之后的版本中可能不需要这步：如果不需要，修改代码，返回完整的消息行列表；

        由于最初的标准是ASCII，latin-1等8比特编码，大概能胜任大多数邮件的解码；这个
        方法应用于整个/全消息文本，而后者其实只是邮件编码故事的一部分：Messages负载和
        Message题头也可能依照email，MIME和Unicode标准进行编码；更多信息请参考mailParser
        与mailSender；
        """
        text = None
        kinds = [self.fetchEncoding]                # 想尝试用户设置
        kinds += ['ascii', 'latin1', 'utf8']        # 再尝试常用类型
        kinds += [sys.getdefaultencoding()]         # 以及操作平台默认设置(因机器而异)
        for kind in kinds:                         # 可能导致邮件保存失败
            try:
                text = [line.decode(kind) for line in messageBytes]
                break
            except (UnicodeError, LookupError):    # LookupError：不好的名字
                pass

        if text is None:
            # 尝试返回题头和错误消息，否则异常可能中止客户端
            # 仍然尝试依照ascii，其它，以及系统平台特异的设置解码题头
            blankline = messageBytes.index(b'')
            hdronly = messageBytes[:blankline]
            commons = ['ascii', 'latin1', 'utf-8']
            for common in commons:
                try:
                    text = [line.decode(common) for line in hdronly]
                    break
                except UnicodeError:
                    pass
            else:                                                  # 都不可行
                try:                                               # 操作平台默认设置?
                    text = [line.decode() for line in hdronly]
                except UnicodeError:
                    text = ['From: (sender of unkown Unicode format headers)']
            text += ['', '--Sorry: mailtools cannot decode this mail content!- -']
        return text

    def downloadMessage(self, msgnum):
        """
        载入给定POP相对消息编号的邮件消息的全部原始文本，调用函数必须解析内容
        """
        self.trace('load' + str(msgnum))
        server = self.connect()
        try:
            resp, msglines, respsz = server.retr(msgnum)
        finally:
            server.quit()
        msglines = self.decodeFulltext(msglines)      # 原始bytes解码成Unicode str
        return '\n'.join(msglines)                    # 连接各行，以便解析

    def downloadAllHeaders(self, progress=None, loadfrom=1):
        """
        获取所有消息或新消息的大小，仅针对原始题头文本开始从消息编号loadfrom载入
        题头，使用loadfrom仅载入新到达邮件，稍后使用downloadMessage获取全部消息
        文本，progress是一个函数，调用形式(count, total)；
        返回：[headers text], [mail sizes], loadedfull?

        添加了mailconfig.fetchlimit以支持大型邮件收件箱：如果不是None,只抓取指定
        数量的题头，将其它邮件作为假/空邮件返回，否则和我的收件箱(4000封)一样的
        收件箱几乎不能用；将loadfrom传给downloadAllMsgs(小漏洞)。
        """
        if not self.srvrHasTop:                     # 并非所有服务器都支持TOP
            # 不作更改，载入所有原始消息文本
            return self.downloadAllMessages(progress, loadfrom)
        else:
            self.trace('loading headers')
            fetchlimit = mailconfig.fetchlimit
            server = self.connect()                  # 邮箱现在处于锁定状态，直到退出
            try:
                resp, msginfos, respsz = server.list()           # 多行'编号大小'组成的列表
                msgCount = len(msginfos)                         # 相当于srvr.stat[0]
                msginfos = msginfos[loadfrom-1:]                 # 去除已经载入的
                allsizes = [int(x.split()[1]) for x in msginfos]
                allhrds = []
                for msgnum in range(loadfrom, msgCount+1):      # 可能是空的
                    if progress:
                        progress(msgnum, msgCount)               # 运行回调函数
                    if fetchlimit and (msgnum <= msgCount - fetchlimit):
                        # 跳过，添加假地址
                        hdrtext = 'Subject: --mail skipped--\n\n'
                        allhrds.append(hdrtext)
                    else:
                        # 抓取，仅提取题头
                        resp, hdrlines, respsz = server.top(msgnum, 0)
                        hdrlines = self.decodeFulltext(hdrlines)
                        allhrds.append('\n'.join(hdrlines))
            finally:
                server.quit()
            assert len(allhrds) == len(allsizes)
            self.trace('load headers exit')
            return allhrds, allsizes, False

    def downloadAllMessages(self, progress=None, loadfrom=1):
        """
        载入编号从loadfrom到N的所有信息的完整信息文本，虽然调用函数可能进行过
        缓存，如果只需题头，比downloadAllHeaders慢得多。

        支持mailconfig.fetchlimit：参考downloadAllHeaders，这里还可以使用server.list()
        获取所跳过的电子邮件的大小，不过大概客户端不关心这些；
        """
        self.trace('loading full messages')
        fetchlimit = mailconfig.fetchlimit
        server = self.connect()
        try:
            msgCount, msgBytes = server.stat()         # 服务器收件箱
            allmsgs = []
            allsizes = []
            for i in range(loadfrom, msgCount+1):     # 如果low >= high, 则内容为空
                if progress:
                    progress(i, msgCount)
                if fetchlimit and (i <= msgCount - fetchlimit):
                    # 跳过，添加假邮件
                    mailtext = 'Subject: --mail skipped--\n\nMail skipped.\n'
                    allmsgs.append(mailtext)
                    allsizes.append(len(mailtext))
                else:
                    # 抓取，提取整封邮件
                    resp, message, respsz = server.retr(i)   # 将文本保存到列表中
                    message = self.decodeFulltext(message)
                    allmsgs.append('\n'.join(message))       # 将邮件留在服务器上
                    allsizes.append(respsz)                  # 与len(msg)不同
        finally:
            server.quit()                                    # 解锁邮箱
        assert len(allmsgs) == msgCount - loadfrom + 1      # 邮件编号从1开始
        # assert sum(allsizes) == msgBytes                   # if loadfrom > 1 则不操作
        return allmsgs, allsizes, True                     # if fetchlimit 则不操作

    def deleteMessages(self, msgnums, progress=None):
        """
        从度武器删除多条消息；假定自从上一次获取/载入消息编号后邮箱未发生变化；
        在消息题头不能用作状态信息时使用；快速，不过可能有风险：参考deleteMessagesSafety
        """
        self.trace('deleting mails')
        server = self.connect()
        try:
            for (ix, msgnum) in enumerate(msgnums):    # 不要每条消息都进行重新连接
                if progress:
                    progress(ix+1, len(msgnums))
                    server.dele(msgnum)
        finally:                                      # 更改消息编号：重新载入
            server.quit()

    def deleteMessagesSafely(self, msgnums, synchHeaders, progress=None):
        """
        从度武器上删除多条消息，不过在删除前使用TOP抓取来检查每条消息的题头部分是否匹配；
        假定电子邮件服务器支持POP的TOP接口，否则抛出TopNotSupported异常 ---- 客户端可以
        调用deleteMessages；在邮件服务器上一次抓取电子邮件索引后可能更爱邮件，以至改变
        POP相对消息编号时使用；如果电子邮件由另一个客户端删除，则可以导致这种情况，此外
        某些ISP可能在下载失败后将邮件箱移动到无法传送邮件箱。
        synchHeaders必须是一个已载入邮件题头文本组成的列表，与选中的邮箱编号想对应(要求
        提供状态)，如果其中任何一个不与电子邮件服务器同步则抛出异常；收件箱在退出前翼子
        锁定，所以TOP检查和实际删除之间应该没有变化；同步化检查必须在这里而非调用函数中
        进行；调用checkSynchError和deleteMessages可能足够，不过在这里检查每条消息，以防
        收件箱中部发生删除和插入；
        """
        if not self.srvrHasTop:
            raise TopNotSupported('Safe delete cancelled')
        self.trace('deletubg mails safely')
        errmsg = 'Message %s out of synch with server.\n'
        errmsg += 'Delete terminated at this message.\n'
        errmsg += 'Mail client may require restart or reload.'
        server = self.connect()                                 # 锁定收件箱，直到退出
        try:                                                    # 不要每条信息都重新连接
            (msgCount, msgBytes) = server.stat()                # 服务器收件箱的大小
            for (ix, msgnum) in enumerate(msgnums):
                if progress:
                    progress(ix + 1, len(msgnums))
                if msgnum > msgCount:                                # 删除了消息
                    raise DeleteSynchError(errmsg % msgnum)
                resp, hdrlines, respsz = server.top(msgnum, 0)       # 只针对题头
                hdrlines = self.decodeFulltext(hdrlines)
                msghdrs = '\n'.join(hdrlines)
                if not self.headersMatch(msghdrs, synchHeaders[msgnum-1]):
                    raise DeleteSynchError(errmsg % msgnum)
                else:
                    server.dele(msgnum)                              # 可以安全删除这条消息
        finally:                                                    # 修改消息编号：重新载入
            server.quit()                                            # 退出时解锁收件箱

    def checkSynchError(self, synchHeaders):
        """
        检查列表synchHeaders中的已载入题头文本是否与服务器上的相匹配，使用POP的TOP命令
        抓取题头文本，在收件箱因其它客户端或邮件服务器自动删除邮件而变化时使用；如果不同
        步则抛出异常，或在与服务器交互式发生错误；

        为速度起见，只检查末尾的最后部分：这样可以探知收件箱的删除，不过假定服务器不会在
        末尾之前插入邮件(对于新到达的邮件的确如此)，首先检查查看收件箱的大小：如果只发生
        过删除则变小；如果发生过删除并且新到达消息添加到尾部，top将变化；结果只在运行时
        才有效：收件箱可能在返回后发生变化；
        """
        self.trace('synch check')
        errormsg = 'Message index out of synch with mail server.\n'
        errormsg += 'Mail client may require restart or reload.'
        server = self.connect()
        try:
            lastmsgnum = len(synchHeaders)                               # 从1到N
            (msgCount, msgBytes) = server.stat()                         # 收件箱大小
            if lastmsgnum > msgCount:                                    # 变小了？
                raise MessageSynchError(errormsg)                       # 没有用于比较的
            if self.srvrHasTop:
                resp, hdrlines, respsz = server.top(lastmsgnum, 0)       # 只针对题头
                hdrlines = self.decodeFulltext(hdrlines)
                lastmsghdrs = '\n'.join(hdrlines)
                if not self.headersMatch(lastmsghdrs, synchHeaders[-1]):
                    raise MessageSynchError(errormsg)
        finally:
            server.quit()

    def headersMatch(self, hdrtext1, hdrtext2):
        """
        可能并非字符串比较这么简单：一些服务器添加"Status:"题头，随时间变化；某家ISP
        的题头为"Status:U"（未读），在抓取后变成"Status:RO"（已读，旧邮件）---- 如果
        在抓取索引时时新邮件，但在删除或上一次消息检查前抓取过则不再处于同步状态；
        "Message-id:"行在理论上对每条消息是唯一的，不过是可选的，可以输入任何字符；
        匹配较常见的：先试：解析消耗大：最后试
        """
        # 尝试通过简单字符串比较做匹配
        if hdrtext1 == hdrtext2:
            self.trace('Same headers text')
            return True

        # 尝试不带状态行做匹配
        split1 = hdrtext1.splitlines()                         # s.split('\n')，但是没有末尾的''
        split2 = hdrtext2.splitlines()
        strip1 = [line for line in split1 if not line.startswith('Status:')]
        strip2 = [line for line in split2 if not line.startswith('Status:')]
        if strip1 == strip2:
            self.trace('Same without Status')
            return True

        # 如果两条消息都有message-id题头，尝试排除匹配
        msgid1 = [line for line in split1 if line[:11].lower() == 'message-id:']
        msgid2 = [line for line in split2 if line[:11].lower() == 'message-id:']
        if (msgid1 or msgid2) and (msgid1 != msgid2):
            self.trace('Different Message-id')
            return False

        # 如果消息id没有或没有，则尝试解析整个题头及常用题头
        tryheaders = ('From', 'To', 'Subject', 'Date')
        tryheaders += ('Cc', 'Return-Path', 'Received')
        msg1 = MailParser().parseHeaders(hdrtext1)
        msg2 = MailParser().parseHeaders(hdrtext2)
        for hdr in tryheaders:                                # 可能接受到多条
            if msg1.get_all(hdr) != msg2.get_all(hdr):         # 大小写敏感，默认为None
                self.trace('Diff common headers')
                return False
            # 所有常用题头匹配而且message-id相同
            self.trace('Same common headers')
            return True

    def getPassword(self):
        """
        如果还没有POP密码则获取之，连接到服务器之前才需要从客户端
        文件或子类方法获取
        """
        if not self.popPassword:
            try:
                localfile = open(mailconfig.poppasswdfile)
                self.popPassword = localfile.readline()[:-1]
                self.trace('local file password' + repr(self.popPassword))
            except:
                self.popPassword = self.askPopPassword()

    def askPopPassword(self):
        assert False, 'Subclass must define method'

########################################################################################
# 专用子类
########################################################################################


class MailFetcherConsole(MailFetcher):
    def askPopPassword(self):
        import getpass
        prompt = 'Password for %s on %s?' % (self.popUser, self.popServer)
        return getpass.getpass(prompt)


class SilentMailFetcher(SilentMailTool, MailFetcher):
    pass  # 替换追踪消息
