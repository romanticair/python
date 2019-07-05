"""API调用，返回Hacker News上当前热门文章的ID，再查看每篇排名靠前的文章"""

import requests
from operator import itemgetter

# 执行API调用并存储响应
url = 'https://hacker-news.firebaseio.com/v0/item/9884165.json'
r = requests.get(url)                                      # 返回当前最热门的500篇文章的ID
print('Status code:', r.status_code)

# 处理有关每篇文章的信息
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:                 # 遍历前30篇文章的ID
    # 对于每篇文章，都执行一个API调用
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
           str(submission_id) + '.json')
    submission_r = requests.get(url)                       # 每篇文章都请求一次
    print('Status code:', submission_r.status_code)
    response_dict = submission_r.json()
    submission_dict = {                                    # 文章标题
        'title': response_dict['title'],                   # 下面是评论页面的链接
        'link': 'http://news.ycombinator.com/v0/item?id=' + str(submission_id),
        'comments': response_dict.get('descendants', 0)    # 文章评论数
    }
    submission_dicts.append(submission_dict)               # 每篇请求过的文章
                                                           # 根据评论次数进行排序
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)
for submission_dict in submission_dicts:
    print('\nTitle', submission_dict['title'])
    print('Discussion:', submission_dict['link'])
    print('Comments:', submission_dict['comments'])


