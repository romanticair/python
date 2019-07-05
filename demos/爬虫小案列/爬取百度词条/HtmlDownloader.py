"""HTML下载器"""

import requests


class HtmlDownloader:
    def download(self, url):
        if url is None:
            return

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
