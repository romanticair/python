"""
XML解析：ElementTree(etree)提供可以解析/生成的、基于Python的API
"""
import pprint
from xml.etree.ElementTree import parse

mapping = {}
tree = parse('books.xml')
for B in tree.findall('book'):
    isbn = B.attrib['isbn']
    for T in B.findall('title'):
        mapping[isbn] = T.text

pprint.pprint(mapping)
