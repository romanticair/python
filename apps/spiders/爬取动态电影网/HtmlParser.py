"""
分为两部分:
    1.从当前网页中提取所有正在上映的电影链接
    2.从动态加载的链接中提取我们所需的字段
"""
# 电影页面链接类似 http://movie.mtime.com/17681/

import re
import json


class HtmlParser:
    def parser_url(self, page_url, response):
        pattern = re.compile(r'http://movie.mtime.com/(\d+)/')
        urls = pattern.findall(response)
        if urls is not None:
            # 将urls进行去重
            return list(set(urls))
        else:
            return None

    def parser_json(self, page_url, response):
        """
        解析响应
        :param page_url:
        :param response:
        :return:
        """
        # 将"="和";"之间的内容提取出来
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(response)[0]
        if result is not None:
            value = json.loads(result)
            try:
                isRelease = value.get('value').get('isRelease')
            except Exception as e:
                print(e)
                return None
            if isRelease:
                if value.get('value').get('hotValue') is None:
                    return self._parser_release(page_url, value)
                else:
                    return self._parser_no_release(page_url, value, isRelease=2)
            else:
                return self._parser_no_release(page_url, value)

    def _parser_release(self, page_url, value):
        """
        解析已经上映的影片
        :param page_url: 电影链接
        :param value: json数据
        :return:
        """
        try:
            isRelease = 1
            MovieRating = value.get('value').get('MovieRating')
            boxOffice = value.get('value').get('boxOffice')
            MovieTitle = value.get('value').get('movieTitle')

            RPictureFinal = MovieRating.get('RPictureFinal')
            RStoryFinal = MovieRating.get('RStoryFinal')
            RDirectorFinal = MovieRating.get('RDirectorFinal')
            ROtherFinal = MovieRating.get('ROtherFinal')
            RatingFinal = MovieRating.get('RatingFinal')

            MovieId = MovieRating.get('movieId')
            Usercount = MovieRating.get('Usercount')
            AttitudeCount = MovieRating.get('AttitudeCount')

            TotalBoxOffice = boxOffice.get('TotalBoxOffice')
            TotalBoxOfficeUnit = boxOffice.get('TotalBoxOfficeUnit')
            TodayBoxOffice = boxOffice.get('TodayBoxOffice')
            TodayBoxOfficeUnit = boxOffice.get('TodayBoxOfficeUnit')
            ShowDays = boxOffice.get('ShowDays')
            try:
                Rank = boxOffice.get('Rank')
            except Exception:
                Rank = 0
            # 返回所提取的内容
            return (MovieId, MovieTitle, RatingFinal, ROtherFinal, RPictureFinal,
                    RDirectorFinal, RStoryFinal, Usercount, AttitudeCount,
                    TotalBoxOffice + TotalBoxOfficeUnit,
                    TodayBoxOffice + TodayBoxOfficeUnit,
                    Rank, ShowDays, isRelease)
        except Exception as e:
            print(e, page_url, value)
            return None

    def _parser_no_release(self, page_url, value, isRelease=0):
        """
        解析未上映的电影信息
        :param page_url:
        :param value:
        :param isRelease:
        :return:
        """
        try:
            MovieRating = value.get('value').get('MovieRating')
            MovieTitle = value.get('value').get('movieTitle')

            RPictureFinal = MovieRating.get('RPictureFinal')
            RStoryFinal = MovieRating.get('RStoryFinal')
            RDirectorFinal = MovieRating.get('RDirectorFinal')
            ROtherFinal = MovieRating.get('ROtherFinal')
            RatingFinal = MovieRating.get('RatingFinal')

            MovieId = MovieRating.get('movieId')
            Usercount = MovieRating.get('Usercount')
            AttitudeCount = MovieRating.get('AttitudeCount')
            try:
                Rank = value.get('value').get('Rank').get('Ranking')
            except Exception:
                Rank = 0
            # 返回所提取的内容
            return (MovieId, MovieTitle, RatingFinal, ROtherFinal, RPictureFinal,
                    RDirectorFinal, RStoryFinal, Usercount, AttitudeCount,
                    u'无', u'无', Rank, 0, isRelease)
        except Exception as e:
            print(e, page_url, value)
            return None
