
# 一些网站反爬虫机制:

"""
1. 分析用户请求的Headers信息进行反爬虫
2. 通过用户行为, 如一个IP在段时间内频繁访问一网站
3. 动态页面增加爬取难度

1) 大多数网站主要是对用户请求的Headers信息"User-Agent"字段进行检测
   简单的伪装只设置"User-Agent"字段信息即可, 高相似度伪装恤将Headers
   中常见字段都设置好
2) 经常切换代理服务器

3) 利用工具软件如: selenium + phantomJS
"""

# 常见字段1 Accept: text/html, application/xhtml+xml, application/xml; q=0.9, */*, q=0.8
# Accept字段只要用表示浏览器能够支持的内容类型, HTML, XHTML, XML三个文档, q为权值系数, 支持优先顺序从左到右

# 常见字段2 Accept-Encoding: gzip, deflate
# 表示浏览器支持的压缩编码, gzip压缩编码其中一种, deflate是无损数据压缩算法

# 常见字段3 Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# 表示浏览器支持的语言类型, zh中文CN简体, en-US(美国)语言, en英语

# 常见字段4 User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0
# 表示用户代理, 服务器可通过该字段识别出客户端浏览器类型版本, 客户端操作系统及其版本号等客户端信息
# Mozilla/5.0 浏览器名及版本信息
# Windows NT 10.0; WOW64; rv:58.0 客户端操作系统信息
# Gecko/20100101 网页排版引擎信息
# Firefox/58.0 火狐浏览器

# 常见字段5 Connection: keep-alive
# 持久性链接, close表示单方面关闭链接, 让链接断开

# 常见字段6 Host:www.youki.com
# 请求服务器网址

# 常见字段7 Referer:网址XXX
# 表示来源网址地址, 从一网址中访问了子页面, 此来源网址为网址XXX

























