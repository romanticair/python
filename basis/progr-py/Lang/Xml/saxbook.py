"""
XML解析： SAX是一个基于回调方法、用于拦截解析器事件的API
"""

import xml.sax, xml.sax.handler, pprint


class BookHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.inTitle = False                       # 处理XML解析器事件
        self.mapping = {}                           # 状态机模型

    def startElement(self, name, attributes):
        if name == 'book':                          # book标签开始
            self.buffer = ''                        # 将ISBN号作为字典的键
            self.isbn = attributes['isbn']
        elif name == 'title':                       # title标签开始
            self.inTitle = True                     # 保存后面的书名文本

    def characters(self, data):
        if self.inTitle:                            # 标签里的文本开始
            self.buffer += data                     # 如果文本在title里，则将其保存

    def endElement(self, name):
        if name == 'title':
            self.inTitle = False                    # title标签结束
            self.mapping[self.isbn] = self.buffer    # 把书名文本存放在字典里


parser = xml.sax.make_parser()
handler = BookHandler()
parser.setContentHandler(handler)
parser.parse('books.xml')
pprint.pprint(handler.mapping)
