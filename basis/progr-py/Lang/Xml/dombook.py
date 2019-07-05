"""
XML解析：DOM将整个文档作为一个可遍历的对象提交给应用程序
"""
import pprint
import xml.dom.minidom
from xml.dom.minidom import Node

doc = xml.dom.minidom.parse('books.xml')         # 将文档载入对象
                                                 # 通常首先就进行解析
mapping = {}
for node in doc.getElementsByTagName('book'):   # 遍历DOM对象
    isbn = node.getAttribute('isbn')             # 通过DOM对象API
    L = node.getElementsByTagName('title')
    for node2 in L:
        title = ""
        for node3 in node2.childNodes:
            if node3.nodeType == Node.TEXT_NODE:
                title += node3.data
        mapping[isbn] = title

# 现在mapping拥有和SAX示例里相同的值
pprint.pprint(mapping)

