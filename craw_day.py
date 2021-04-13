import time
import os
import pandas

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process

# 这个是一个用来控制chrome以无界面模式打开的浏览器
# 创建一个参数对象，用来控制chrome以无界面的方式打开
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# 后面的两个是固定写法 必须这么写
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


class MultiProcessDayCrawler(Process):

    def __init__(self, year, month, day):
        super(MultiProcessDayCrawler, self).__init__()
        self.year = year
        self.month = month
        self.day = day

    def run(self):
        browser = webdriver.Chrome(options=chrome_options)
        date = '{:}-{:}-{:}'.format(self.year, self.month, self.day)
        save_path = os.path.join('day_csv', date + '-weather.csv')
        if not os.path.isdir('day_csv'):
            os.mkdir('day_csv')
        column_name = ['Time', 'Temperature',
                       'Dew Point', 'Humidity',
                       'Wind', 'Wind Speed',
                       'Wind Gust', 'Pressure',
                       'Precipitation', 'Condition',
                       ]
        url = 'https://www.wunderground.com/history/daily/us/ny/new-york-city' \
              'KLGA/date/{:}'.format(date)
        browser.get(url)
        time.sleep(20)          # 使数据完整，否则可能缺少数据
        table = browser.find_element_by_xpath("//table[@class='mat-table cdk-table mat-sort ng-star-inserted']")
        # tbody = table.find_element_by_tag_name('tbody')
        td_list = table.find_elements_by_xpath("tbody/tr/td")
        data_of_day = []
        for td in td_list:
            line_test = td.text.strip()
            data_of_day.append(line_test)
        data_frame = []
        row_index = 0
        row_data = []
        for data in data_of_day:
            row_data.append(data)
            row_index += 1
            if row_index == 10:
                data_frame.append(row_data.copy())
                row_data = []
                row_index = 0
        data_frame = pandas.DataFrame(data_frame, columns=column_name)
        data_frame.to_csv(save_path)
        if len(data_of_day) < 240:
            print("Date: {}, len: {}".format(date, len(data_of_day)))
        else:
            print("Successful saved a file: {}!".format(save_path))
        browser.quit()


if __name__ == '__main__':
    # 可以多进程
    p = MultiProcessDayCrawler(2018, 10, 1)
    p.start()