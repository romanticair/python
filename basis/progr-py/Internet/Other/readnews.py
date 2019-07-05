"""
借助nntplib模块，从comp.lang.python抓取并打印usenet新闻组文章，模块运行在套接字至上。
nntplib还支持发布新消息等；注：读取消息后并不将其删除；
"""
import sys
from nntplib import NNTP

listonly = False
showhdrs = ['From', 'Subject', 'Date', 'Newsgroups', 'Lines']
try:
    servername, groupname, showcount = sys.argv[1:]
    showcount = input(showcount)
except:
    servername = 'news.rmi.net'                # 把它复制给你的服务器
    groupname = 'com.lang.python'              # 命令行参数或默认值
    showcount = 10                             # 显示最新的showcount条消息

# 连接到nntp服务器
print('Connecting to', servername, 'for', groupname)
connection = NNTP(servername)
reply, count, first, last, name = connection.group(groupname)
print('%s has %s articles: %s-%s' % (name, count, first, last))

# 只请求题头
fetchfrom = str(int(last) - (showcount - 1))
reply, subjects = connection.xhdr('subject', (fetchfrom + '-' + last))

# 显示题头，获取消息的题头和主体
for (id, subj) in subjects:                   # [-showcount:] if fetch all hdrs
    print('Article %s [%s]' % (id, subj))
    if not listonly and input('=>Display?') in ['y', 'Y']:
        reply, num, tid, list = connection.head(id)
        for line in list:
            for prefix in showhdrs:
                if line[:len(prefix)] == prefix:
                    print(line[:80])
                    break
        if input('=> Show body?') in ['y', 'Y']:
            reply, num, tid, list = connection.body(id)
            for line in list:
                print(line[:80])

    print()

print(connection.quit())

# localfile = open('filenmae')   # 文件已有合适的题头
# connection.post(localfile)     # 将文本发送到新闻组
