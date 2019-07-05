"""
发送消息，添加附件
"""

import os
import smtplib
import mimetypes                                     # mimetypes: 文件名到类型
import email.utils, email.encoders                   # 日期字符串，base64格式
from email.message import Message                    # 普通消息，对象->文本
from email.mime.multipart import MIMEMultipart       # 类型特异的消息
from email.mime.audio import MIMEAudio               # 格式化/编码附件
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication   # 使用新app类
import Internet.Email.mailconfig as mailconfig       # 客户端的mailconfig
from .mailTool import MailTool, SilentMailTool       # 包相对路径


def fix_encode_base64(msgobj):
    """
    对于Python3.1 email包里不能从base64或其它email编码格式编码的二进制部分，
    生成邮件文件漏洞的规避措施，构造器运行的正常的email.encoder即便在负载编码
    为base64文本后，仍将其保留为bytes类型；这样打断了邮件文本的生成，后者假定其
    为文本形式而且要求其为str类型；总的结果是只有简单的文本部分邮件可用Py3.1 email
    包不加改动而成功撰写 ---- 任何MIME编码的二进制部分将致使邮件文本生成失败；这个
    bug看起来会在以后的Python和email包版本中得到纠正，到那时这一步应该可以取消；
    """
    linelen = 76                             # 按照MIME标准的规定
    from email.encoders import encode_base64

    encode_base64(msgobj)                    # email的通常做法，保留为bytes类型
    text = msgobj.get_payload()              # bytes在email包进行文本生成时导致失败
    if isinstance(text, bytes):              # 负载在3.1中为bytes类型，3.2 alpha中为str
        text = text.decode('ascii')          # 解码成Unicode str以便进行文本生成
    lines = []                               # 分割成多行，否则是很长的一行
    text = text.replace('\n', '')            # 3.1中没有\n，不过该项去官网检查
    while text:
        line, text = text[:linelen, linelen:]
        lines.append(line)
    msgobj.set_payload('\n'.join(lines))


def fix_text_required(encodingname):
    """
    email包里的str/bytes组合错误的规避措施，由于MIME编码某些文本中某些类型
    的方式不同，Python3.1中MIMEText对不同Unicode编码要求不同的类型，唯一的
    替代方案是使用通用Message并重复其中大部分代码；
    """
    from email.charset import Charset, BASE64, QP

    charset = Charset(encodingname)          # email如何探知，怎样进行编码
    bodyenc = charset.body_encoding          # utf8，其它编码要求bytes类型输入数据
    return bodyenc in (None, QP)           # ascii, latin1, 其它编码要求str


class MailSender(MailTool):
    """
    发送邮件：格式化一条信息，与SMTP服务器建立接口；可在任何带有Python和Internet的
    机器上运行，而不需要使用cmdline邮件；不要求验证的客户端：如果要求登录验证，请参
    考MailSenderAuth；trancesize是代表被追踪的消息文本的数字字符串：0=没有，big=所有；
    支持文本主体和文本部分的Unicode编码，支持题头的编码，包括完整题头和电子邮件姓名；
    """
    def __init__(self, smtpserver=None, tracesize=256):
        self.smtpServerName = smtpserver or mailconfig.smtpservername
        self.tracesize = tracesize

    def sendMessage(self, From, To, Subj, extrahdrs, bodytext, attaches,
                    saveMailSeparator=(('=' * 80) + 'PY\n'),
                    bodytextEncoding='us-ascii',
                    attachesEncodings=None):
        """
        格式化并发送邮件：阻塞调用函数，在GUI里把我作为线程，bodytext是主体文本部分，
        attaches是文件名组成的列表，extrahdrs是(姓名，值)元组构成的列表，如果任何原因
        导致发送失败，则抛出不被捕获的异常，如果成功，则在本地文件中保存已发送的消息文
        本，假定收件人、抄送、密送题头值为一到多个已知编码好的地址组成的列表(格式可能是
        完整的姓名+<地址>格式)，客户端必须对它们进行解析，以分割符做分割，或者使用多行输
        入，请注意SMTP允许收件人使用完整的姓名+<地址>格式。现在密送用于发送/信封，不过去除了题头，移除了重复的收件人，否则将得到多份邮件副
        本。
        缺陷：不支持多组分/可替代组分邮件，直蹦混合；
        """
        # 假定主题文本已经编码为目标形式
        # 客户端可以将解码为用户选定的，默认的，或utf-8备用编码形式
        # 不论哪种操作，email需要相应的str异或bytes类型

        if fix_text_required(bodytextEncoding):
            if not isinstance(bodytext, str):
                bodytext = bodytext.decode(bodytextEncoding)
        else:
            if not isinstance(bodytext, bytes):
                bodytext = bodytext.encode(bodytextEncoding)

        # 创建基本消息
        if not attaches:
            msg = Message()
            msg.set_payload(bodytext, charset=bodytextEncoding)
        else:
            msg = MIMEMultipart()
            self.addAttachments(msg, bodytext, attaches, bodytextEncoding, attachesEncodings)

        # 非ASCII题头在发送时进行编码，只编码地址里的姓名，
        # 否则smtp彻底放弃消息；
        # 编码所有信封，包括收件姓名(而非地址)，并假定服务器运行此操作
        # msg.as_string保留题头编码所添加的任何换行符
        hdrenc = mailconfig.headersEncodeTo or 'utf-8'         # default=utf8
        Subj = self.encodeHeader(Subj, hdrenc)                 # 完整题头
        From = self.encodeAddrHeader(From, hdrenc)             # 电子邮件姓名
        To = [self.encodeAddrHeader(T, hdrenc) for T in To]   # 各收件人
        Tos = ', '.join(To)                                    # 题头+信封

        # 将题头添加至基本消息
        msg['From'] = From
        msg['To'] = Tos                               # 可能有多个地址列表
        msg['Subject'] = Subj                         # 服务器拒绝以';'为分隔符
        msg['Date'] = email.utils.formatdate()        # 当前日期时间，rfc2822 utc
        recip = To
        for name, value in extrahdrs:                # 抄送，密送，X-Mailer，等等
            if value:
                if name.lower() not in ['cc', 'bcc']:
                    value = self.encodeHeader(value, hdrenc)
                    msg[name] = value
                else:
                    value = [self.encodeAddrHeader(v, hdrenc) for v in value]
                    recip += value                    # 有些服务器拒绝['']
                if name.lower() != 'bcc':             # 密送获取邮件，不带题头
                    msg[name] = ', '.join(value)      # 在各抄送间添加逗号
        recip = list(set(recip))                      # 移除重复项
        fullText = msg.as_string()                    # 生成格式化后的消息

        # 如果所有Tos都失败sendmail调用将抛出异常，或
        # 返回含有所有失败发送的Tos字典
        self.trace('Sending to...' + str(recip))
        self.trace(fullText[:self.tracesize])         # SMTP调用进行连接
        server = smtplib.SMTP_SSL(self.smtpServerName, timeout=20)
        server.login('user_siri@foxmail.com', 'uebgvreobstidicb')   # 匿名居然用不了???
        # server = smtplib.SMTP(self.smtpServerName)  # 此操作可能失败
        # server.login('anonymous', '')
        self.getPassword()                            # 如果服务器要求
        self.authenticateServer(server)               # 在子类中登录
        try:
            failed = server.sendmail(From, recip, fullText)  # 异常或返回字典
        except:
            server.close()                                   # quit可能导致挂断
            raise                                           # 再次抛出异常
        else:
            server.quit()                                    # 连接+发送均ok
        self.saveSentMessage(fullText, saveMailSeparator)    # 首先进行此操作
        if failed:
            class SomeAddrsFailed(Exception):
                pass
            raise SomeAddrsFailed('Failed addrs:%s\n' % failed)
        self.trace('Send exit')

    def addAttachments(self, mainmsg, bodytext, attaches, bodytextEncoding, attachesEncodings):
        """
        格式化一条带有附件的多部分组成的消息，如果传入文本部分，则对其使用Unicode编码；
        """
        # 添加主题文本/纯文本部分
        msg = MIMEText(bodytext, _charset=bodytextEncoding)
        mainmsg.attach(msg)
        # 添加附件部分
        encodings = attachesEncodings or (['us-ascii'] * len(attaches))
        for (filename, fileencode) in zip(attaches, encodings):
            # 文件名可能是绝对或相对路径
            if not os.path.isfile(filename):                   # 跳过目录，等等
                continue

            # 根据文件后缀名推测内容类型，忽略编码
            contype, encoding = mimetypes.guess_type(filename)
            if contype is None or encoding is not None:      # 不做推测，是否压缩文件?
                contype = 'application/octet-stream'            # 使用通用默认值
            self.trace('Adding' + contype)

            # 组件合适类型的Message子类
            maintype, subtype = contype.split('/', 1)
            if maintype == 'text':                              # 文本需要编码
                if fix_text_required(fileencode):               # 要求str或bytes
                    data = open(filename, 'r', encoding=fileencode)
                else:
                    data = open(filename, 'rb')
                msg = MIMEText(data.read(), _subtype=subtype, _charset=fileencode)
                data.close()
            elif maintype == 'image':
                data = open(filename, 'rb')                     # 使用二进制补丁
                msg = MIMEImage(data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()
            elif maintype == 'audio':
                data = open(filename, 'rb')
                msg = MIMEAudio(data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()
            elif maintype == 'application':
                data = open(filename, 'rb')
                msg = MIMEApplication(data.read(), _subtype=subtype, _encoder=fix_encode_base64)
                data.close()
            else:
                data = open(filename, 'rb')                    # application/*也可以
                msg = MIMEBase(maintype, subtype)              # 使用此代码
                msg.set_payload(data.read())
                data.close()                                   # 创建通用类型
                fix_encode_base64(msg)                         # 上次在此再次中断!
                # email.encoders.encode_base64(msg)            # 使用base64编码

            # 设置文件名并添加到容器
            basename = os.path.basename(filename)
            msg.add_header('Content-Disposition', 'attachments', filename=basename)
            mainmsg.attach(msg)

        # mime结构之外的文本，非MIME邮件阅读器可阅读的部分
        mainmsg.preamble = 'A multi-part MIME format message.\n'
        mainmsg.epilogue = ''                                 # 确保消息末尾带有换行符

    def saveSentMessage(self, fullText, saveMailSeparator):
        """
        如果任何消息发送成，将其追加到本地文件末尾。
        客户端：传入你的应用程序使用的分隔符，做分割。
        缺陷：同时用户可能在更改这个文件(可能性不大)。
        """
        try:
            sentfile = open(mailconfig.savemailfile, 'a', encoding=mailconfig.fetchEncoding)
            if fullText[-1] != '\n':
                fullText += '\n'
            sentfile.write(saveMailSeparator)
            sentfile.write(fullText)
            sentfile.close()
        except:
            self.trace('Could not save sent message')        # 不至于使好戏崩溃退出

    def encodeHeader(self, headertext, unicodeencoding='utf-8'):
        """
        按照可选的用户设置或UTF-8，参照email或Unicode标准码撰写好的非ascii
        消息题头内容，如有必要，header.encode在题头字符串中自动添加换行符。
        """
        try:
            headertext.encode('ascii')
        except:
            try:
                hdrobj = email.header.make_header([(headertext, unicodeencoding)])
                headertext = hdrobj.encode()
            except:
                pass                      # 如有必要，自动分割成多行内容
        return headertext                 # 如果没有编码或ascii，可能引起smtplib操作失败

    def encodeAddrHeader(self, headertext, unicodeencoding='utf-8'):
        """
        依照电子邮件，MIME和Unicode标准尝试编码电子邮件地址中的非ASCII姓名，如果
        失败，则省略名称而只使用地址部分，如果连地址都无法获取，尝试作为整体一起
        解码，否则smtplib在尝试将整个邮件作为ASCII而编码时可能发生错误；
        utf-8格式化代码使用范围较广，应该能够胜任多数情况；如果过长则插入换行符，
        hrd, encode分割姓名时也将得到多行结果，不过行的长度大于临界值，可能捕获不
        到（有待改进），这里使用Message.as_string格式化代码时不做进一步拆行，mailParser
        模块里的decodeAddrHeader是它的逆向操作。
        """
        try:
            pairs = email.utils.getaddresses([headertext])    # 分割 地址+邮件部分
            encoded = []
            for name, addr in pairs:
                try:
                    name.encode('ascii')                      # 如果ascii编码可行则不加更改即使用
                except UnicodeError:                         # 否则尝试编码姓名部分
                    try:
                        uni = name.encode(unicodeencoding)
                        hdr = email.header.make_header([uni, unicodeencoding])
                        name = hdr.encode()
                    except:
                        name = None                            # 省略名字，只使用地址部分
                joined = email.utils.formataddr((name, addr))   # 如有必要则引用名字
                encoded.append(joined)

            fullhrd = ', '.join(encoded)
            if len(fullhrd) > 72 or '\n' in fullhrd:         # 不是一行短字符串?
                fullhrd = ',\n'.join(encoded)                 # 尝试多行
            return fullhrd
        except:
            return self.encodeHeader(headertext)

    def authenticateServer(self, server):
        pass                                                 # 这个服务器/类不要求登录

    def getPassword(self):
        pass

####################################################################################
# 专用子类
####################################################################################


class MailSenderAuth(MailSender):
    """
    用于要求登录验证的子类：客户端选择基于mailconfig.smtpuser设置(可能为None?)的
    MailSender或MailSenderAuth超类。
    """
    smtpPassword = None                         # 作为一个类，而非放在self中，可能被多个实例共享

    def __init__(self, smtpserver=None, smtpuser=None, tracesize=None):
        MailSender.__init__(self, smtpserver, tracesize)
        self.smtpUser = smtpuser or mailconfig.smtpuser
        # self.smtpPassword = None              # 每次发送都让PyMailGUI做请求!

    def authenticateServer(self, server):
        server.login(self.smtpUser, self.smtpPassword)

    def getPassword(self):
        """
        如果还没有SMTP验证密码则获取之，可能由超类自动调用或客户端收的调用：在
        发送前不需要，不过不在GUI线程里运行，从客户端文件或子类方法获取
        """
        if not self.smtpPassword:
            try:
                localfile = open(mailconfig.smtppasswdfile)
                MailSenderAuth.smtpPassword = localfile.readline()[:-1]
                self.trace('local file password' + repr(self.smtpPassword))
            except:
                MailSenderAuth.smtpPassword = self.askSmtpPassword()

    def askSmtpPassword(self):
        assert False, 'Subclass must define method'


class MailSenderAuthConsole(MailSenderAuth):
    def askSmtpPassword(self):
        import getpass
        prompt = 'Password for %s on %s' % (self.smtpUser, self.smtpPassword)
        return getpass.getpass(prompt)


class SilentMailSender(SilentMailTool, MailSender):
    pass  # 替换追踪信息
