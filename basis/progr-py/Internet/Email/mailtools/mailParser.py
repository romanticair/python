"""
解析及附件提取，分析，保存
"""
import os
import sys
import mimetypes                         # 将类型映射为文件名
import email.parser                      # 将文本解析为Message对象
import email.header                      # 题头解码/编码
import email.utils                       # email.message地址题头解析/解码
from email.message import Message        # Message可以遍历
from .mailTool import MailTool           # 包相对路径


class MailParser(MailTool):
    """
    解析消息文本和附件的方法
    微妙细节：对于非多组分的消息，Message对象负载是一个简单的字符串，对于多组分消息，它
    是Message对象组成的列表(可能拥有嵌套结构)，这里我们无须区别对待这两种情况，因为Message
    遍历生成器总是先返回自身，因此对于非多组分消息也可以运行无误(遍历了单个对象)；

    对于简单消息，这里总是把消息看成邮件的一部分；对于多组分消息，组分列表包含主体消息文本
    及所有附件；这样使得不属于类型文本的简单消息在UI中当作附件来处理(如保存，打开)；对于
    某些不常见的组分类型，Message负载也有可能为None；

    Py3.1中，使用decode=1时将文本组分的负载作为bytes返回，否则肯恩是str；在mailtools中，文件
    保存时将文本存储为bytes，而主文本字节负载则依照邮件题头信息或操作平台默认值及推测结果
    解码为Unicode str；客户端可能需要转换其它负载：PyMailGUI利用题头解码保存到二进制文件的组
    分；

    支持基于抓取来的消息内容的自动解码，包括Subject等厂家题头及From和To等地质题头中的姓名：
    客户端必须在解析后请求此操作；解析器在显示之前不进行解码；
    """
    def walkNamedParts(self, message):
        """
        为避免重复组分命名逻辑的生成器；跳过多组分消息的题头，生成组分文件名；消息
        已经在解析好的email.message.Message对象中；不跳过罕见类型：负载可能为None，
        必须在组分保存时予以处理；某些其它情况可能也可以跳过；
        """
        for (ix, part) in enumerate(message.walk()):         # 遍历包括消息
            fulltype = part.get_content_type()                # ix包括跳过的组分
            maintype = part.get_content_maintype()
            if maintype == 'multipart':                       # multipart/*:容器
                continue
            elif fulltype == 'message/rfc822':               # 跳过message/rfc822
                continue                                     # 跳过所有message/*?
            else:
                filename, contype = self.partName(part, ix)
                yield filename, contype, part

    def partName(self, part, ix):
        """
        从消息组分中提取文件名和内容类型；
        文件名：尝试Content-Disposition名称参数，然后尝试Content-Type。或者根据
        mimetype推测结果生成文件名；
        """
        filename = part.get_filename()                    # 文件名在消息题头中?
        contype = part.get_content_type()                 # 主类/亚类为小写
        if not filename:
            filename = part.get_param('name')             # 尝试content-type名
        if not filename:
            if contype == 'text/plain':                   # 硬编码纯文本后缀名
                ext = '.txt'                              # 不然就猜它是.ksh!
            else:
                ext = mimetypes.guess_extension(contype)
                if not ext:                               # 使用通用默认设置
                    ext = '.bin'
            filename = 'part-%03d%s' % (ix, ext)
        return self.decodeHeader(filename), contype

    def saveParts(self, savedir, message):
        """
        将消息的所有部分保存为本地目录下的多个文件；
        返回(['maintype/subtype', 'filename'])列表以供调用函数使用，不过这里不打开任何
        组分或附件；
        get_paykiad解码base64、quoted-printable和uuencoding编码的数据；
        对于罕见类型，邮件解析器可能给我们返回一个None负载，大概应该跳过：这里为了保险
        将其转换为str;
        """
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        partfiles = []
        for (filename, contype, part) in self.walkNamedParts(message):
            fullname = os.path.join(savedir, filename)
            fileobj = open(fullname, 'wb')              # 使用二进制模式
            content = part.get_payload(decode=1)        # 解码base64、quoted-printable和uuencoding编码
            if not isinstance(contype, bytes):         # 打开文件的rb参数需要bytes
                content = b'(no content)'               # decode=1返回bytes
            fileobj.write(content)                      # 不过某些负载返回None
            fileobj.close()                             # 不采用str(content)
            partfiles.append((contype, fullname))       # 供调用函数打开
        return partfiles

    def saveOnePart(self, savedir, partname, message):
        """
        同上，不过只根据名称查找和保存一个部分
        """
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        fullname = os.path.join(savedir, partname)
        (contype, content) = self.findOnePart(partname, message)
        if not isinstance(content, bytes):           # 打开文件的rb参数需要bytes
            content = b'(no content)'                 # decode=1返回bytes
        open(fullname, 'wb').write(content)           # 不过某些负载返回bytes
        return contype, fullname                     # 不采用str(content)

    def partsList(self, message):
        """
        返回列表，由已解析的消息的所有部分的文件名组成，和saveParts使用相同文件名
        逻辑，不过这里不保存组分文件
        """
        validParts = self.walkNamedParts(message)
        return [filename for (filename, contype, part) in validParts]

    def findOnePart(self, partname, message):
        """
        查找并返回给定名称的组分的内容；
        用来与partsList分配使用；
        在这里我们也可以采用mimetypes.guess_type(partname)；
        我们还能通过保存到字典而避免这个搜索操作；
        内容可能为str或bytes ---- 必要时转换；
        """
        for (filename, contype, part) in self.walkNamedParts(message):
            if filename == partname:
                content = part.get_payload(decode=1)   # 解码base64,quoted-printable,uuencoding
                return contype, content               # 可能为bytes文本

    def decodePayload(self, part, asStr=True):
        """
        将文本组分bytes解码为Unicode str，以便显示、自动换行等；组分是一个Message
        对象，(decode=1)则取消MIME邮件编码(base64,quoted-printable和uuencoding编码)，
        bytes.decode()进行额外的Unicode文本字符串解码；首先尝试消息题头中的字符集编码
        名称(如果有且正确)，然后尝试操作平台默认值及尝试推测数次，最后放弃，返回错误
        字符串。
        """
        payload = part.get_payload(decode=1)              # 负载可能是bytes
        if asStr and isinstance(payload, bytes):         # decode=1返回bytes
            tries = []
            enchdr = part.get_content_charset()           # 想尝试消息题头
            if enchdr:
                tries += [enchdr]                         # 想尝试题头
            tries += [sys.getdefaultencoding()]           # 相当于bytes.decode()
            tries += ['latin1', 'utf8']                   # 尝试8比特编码，包括ascii
            for t in tries:                              # 尝试utf8
                try:
                    payload = payload.decode(t)           # 试一试
                    break
                except (UnicodeError, LookupError):      # LookupError: 不好的名字
                    pass
            else:
                payload = '--sorry: cannot decode Unicode text--'
        return payload

    def findMainText(self, message, asStr=True):
        """
        对于面向对文本的客户端，返回首个文本组分的str，对于简单消息的负载或多组分消息
        的所有部分，查找text/plain，然后查找text/html，接着查找text/*，最后断定没有文
        本可显示；这个操作时一个试探过程，不过能应付大多数简单的、multipart/alternative
        和multipart/mixed信息；如果简单消息中没有，则content-type默认为text/plain；

        通过遍历而非列表扫描处理最高层次的嵌套；如果是非多组分消息但类型为text/html，
        返回HTML,因为文本带有HTML类型，调用函数可能用网页浏览器打开，提取纯文本，等
        等，如果是非多组分消息而且不是文本，那么没有文本可显示：在UI中保存/打开消息内
        容，缺陷：没有尝试将类型的text/plain的部分的数行连接在一起；
        文本负载可能为bytes ---- 在此解码为str;
        保存HTML文件时使用asStr=False以获取原始字节
        """
        # 尝试查找纯文本
        for part in message.walk():                           # 遍历访问消息
            type = part.get_content_type()                     # 如果是非多组分消息
            if type == 'text/plain':                           # 可能是base64,quoted-printable,uuencoding
                return type, self.decodePayload(part, asStr)  # 也进行bytes到str的转换?

        # 尝试查找HTML组分
        for part in message.walk():
            type = part.get_content_type()                     # 调用函数渲染html
            if type == 'text/html':
                return type, self.decodePayload(part, asStr)

        # 尝试任何其他类型，包括XML
        for part in message.walk():
            maintype = part.get_content_maintype()
            type = part.get_content_type()
            if maintype == 'text':
                return type, self.decodePayload(part, asStr)

        # 赌博做法：可以使用首个组分，不过它还没有被标记为文本
        failtext = '[No text to display]' if asStr else b'[No text to display]'
        return 'text/plain', failtext

    def decodeHeader(self, rawheader):
        """
        根据其内容，依照电子邮件和Unicode标准解码已有的国际化题头文本；如果未被
        编码或解码失败，按原样返回；
        客户端必须调用这个函数来显示信息：解析得到Message对象不进行解码；
        国际化题头示例：
        '=?UTF-8?Q?Introducing=20Top=20Values=20..Savers?=';
        国际化题头示例：
        'Man where did you get that =?UTF-8?Q?assistant=3F?=';

        decode_header自动处理题头字符串中的任何换行，如果题头的任何子字符串被编码，
        则可能返回多个组分，如果找到任何编码名称则在组分列表中返回所有bytes（未编码组分
        编码为raw-unicode-escape格式且enc=None）,然而如果整个题头均未经过编码，则在enc=None
        时在Py3.1中返回单独一个部分，类型为str而非bytes（这里必须对混合类型做处理）；

        以下代码属于最初的尝试，只要没有经过编码的子字符串，或者enc作为None返回(抛出异常，
        返回做改变的原始题头)，那么可以成功运行：
        hdr, enc = email.header.decode_header(rawheader)[0]
        return hrd.decode(enc) # 如果enc=None则失败：没有编码名称或经过编码的子字符串
        """
        try:
            parts = email.header.decode_header(rawheader)
            decoded = []
            for (part, enc) in parts:                   # 对于所有子字符串
                if enc is None:                         # 组分未经编码?
                    if not isinstance(part, bytes):     # str: 整个题头未经比啊那么
                        decoded += [part]                # 否则进行unicode解码
                    else:
                        decoded += [part.decode('raw-unicode-escape')]
                else:
                    decoded += [part.decode(enc)]
            return ' '.join(decoded)
        except:
            return rawheader                            # 搏一把!

    def decodeAddrHeader(self, rawheader):
        """
        根据其内容，依照电子邮件和Unicode标准解码已有的国际化题头文本；必须解析电子邮件
        地址的第一个部分以获取国际化部分：'"=?UTF-8?Walmart?="<newsletters@walmart.com>'；
        From大概只有一个地址，不过To、CC和Bcc可能有多个；

        decodeHeader处理完整题头内嵌套着编码过的子字节串，不过这里我们不能简单地对于整个
        题头调用这个函数，因为如果编码后的名称字符串以"引号而非泛空格符或首位字符串结尾的
        话，这个函数将允许失败；mailSender模块中的encodeAddrHeader是这个函数的逆向操作；"

        以下代码属于最初的尝试，如果存在编码过的子字符串，将在处理姓名中的编码过的子字符
        串时失败，并针对未编码的bytes部分抛出异常；
        namebytes, nameenc = email.header.decode_header(name)[0] (do email+MIME)
        if nameenc: name = namebytes.decode(nameenc) (do Unicode?)
        """
        try:
            pairs = email.utils.getaddresses([rawheader])         # 分割地址和组分
            decoded = []                                          # 处理姓名中的逗号
            for (name, addr) in pairs:
                try:
                    name = self.decodeHeader(name)                # 电子邮件+MIME+Unicode
                except:
                    name = None                                  # 如果decodeHeader抛出异常则使用编码过的姓名
                joined = email.utils.formataddr((name, addr))     # 合并各部分
                decoded.append(joined)
            return ', '.join(decoded)                             # >= 1地址
        except:
            return self.decodeHeader(rawheader)                  # 尝试解码整个字符串

    def splitAddresses(self, field):
        """
        在UI中对于多个地址使用逗号分隔符，使用getaddresses来正确进行分割并允许
        地址的姓名部分中使用逗号，PyMailGUI在必要时使用它来分割由用户输入和题头
        复制得到的收件人、抄送、密送；如果域为空或碰到了一场，则返回空列表；
        """
        try:
            pairs = email.utils.getaddresses([field])                 # [(姓名，地址)]
            return [email.utils.formataddr(pair) for pair in pairs]  # [(姓名，地址)]
        except:
            return ''          # 用户输入域中句法错误？或者其它错误

    # 解析失败时的返回
    errorMessage = Message()
    errorMessage.set_payload('[Unalbe to parse message - format error]')

    def parseHeaders(self, mailtext):
        """
        仅解析题头，返回email.message.Message根对象，在题头解析后停止，即便后面
        没有东西(top)email.message.Message对象包含邮件题头域的映射关系消息对象的
        负载为None,而非原始主体文本；
        """
        try:
            return email.parser.Parser().parsestr(mailtext, headersonly=True)
        except:
            return self.errorMessage

    def parseMessage(self, fulltext):
        """
        解析整个消息，返回email.message.Message根对象，如果不采用is_multipart(),
        消息对象的负载是一个字符串，如果含有多个组分，那么消息对象的负载是其它Message
        对象，这个调用相当于email.message_from_string()
        """
        try:
            return email.parser.Parser().parsestr(fulltext)   # 可能失败!
        except:
            return self.errorMessage                          # 或者让调用函数来处理?可检查返回值

    def parseMessageRaw(self, fulltext):
        """
        只解析题头，返回email.message.Message根对象
        出于运行效率考虑，在题头解析后停止(这里还没用上)消息对象
        的负载是题头之后的邮件原始文本
        """
        try:
            return email.parser.HeaderParser().parsestr(fulltext)
        except:
            return self.errorMessage
