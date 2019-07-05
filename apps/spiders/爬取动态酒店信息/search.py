import time
import codecs
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class QunaSpider:
    def get_hotel(self, driver, to_city, fromdate, todate):
        # 搜素前的页面，获取元素位置，以便访问
        ele_toCity = driver.find_element_by_name('toCity')
        ele_fromDate = driver.find_element_by_id('fromDate')
        ele_toDate = driver.find_element_by_id('toDate')
        ele_search = driver.find_element_by_class_name('search-btn')

        ele_toCity.clear()
        ele_toCity.send_keys(to_city)
        ele_toCity.click()
        ele_fromDate.clear()
        ele_fromDate.send_keys(fromdate)
        ele_toDate.clear()
        ele_toDate.send_keys(todate)
        ele_search.click()

        # 点击搜索之后的页面
        page_num = 0
        while True:
            # 下拉到底部,获取完整的数据
            try:
                WebDriverWait(driver, 10).until(EC.title_contains(to_city))
            except Exception as e:
                print(e)
                if page_num > 5:
                    break

            time.sleep(5)
            try:
                js = 'window.scrollTo(0, document.body.scrollHeight);'
                driver.execute_script(js)
            except Exception as e:
                print(e)

            time.sleep(5)
            # 解析酒店信息，将数据进行清洗和存储
            htm_const = driver.page_source
            soup = BeautifulSoup(htm_const, 'html.parser', from_encoding='utf-8')
            infos = soup.find_all(class_='item_hotel_info')

            # 输出到文件
            f = codecs.open(to_city + fromdate + '.html', 'a', 'utf-8')
            for info in infos:
                f.write(str(page_num) + '--' * 50)
                content = info.get_text().replace(' ', '').replace('\t', '').strip()
                for line in [ln for ln in content.splitlines() if ln.strip()]:
                    f.write(line)
                    f.write('\r\n')
            f.close()

            # 点击下一页，继续重复这一过程
            try:
                next_page = WebDriverWait(driver, 10).until(EC.visibility_of(
                    driver.find_element_by_css_selector('.item.next')))
                next_page.click()
                page_num += 1
                time.sleep(10)
            except Exception as e:
                print(e)
                if page_num > 5:
                    break

    def crawl(self, root_url, to_city):
        """只采取当天的酒店信息"""
        today = datetime.date.today().strftime('%Y-%m-%d')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        driver = webdriver.Firefox()
        # 如果浏览器驱动不在环境里
        # driver = webdriver.Firefox(executable_path='F:\python\geckodriver.exe')
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.maximize_window()     # 将浏览器最大化显示
        driver.implicitly_wait(10)   # 控制健个身时间，等待浏览器反映
        self.get_hotel(driver, to_city, today, tomorrow)


if __name__ == '__main__':
    url = 'http://hotel.qunar.com/'
    to = '深圳'
    spider = QunaSpider()
    spider.crawl(url, to)
