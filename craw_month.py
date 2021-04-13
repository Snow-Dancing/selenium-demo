import time
import os
import pandas
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 这个是一个用来控制chrome以无界面模式打开的浏览器
# 创建一个参数对象，用来控制chrome以无界面的方式打开
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# 后面的两个是固定写法 必须这么写
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


def save_source_page(source_page, path):
    with open(path, 'w', encoding='utf8') as f:
        f.write(source_page)


def craw_month_weather_data(year, month):
    browser = webdriver.Chrome(options=chrome_options)
    date = '{:}-{:}'.format(year, month)
    save_path = os.path.join('month_csv', date + '-weather.csv')
    if not os.path.isdir('month_csv'):
        os.mkdir('month_csv')
    column_name = ['Day',
                   'Tem_Max', 'Tem_Avg', 'Tem_Min',
                   'Dew_Max', 'Dew_Avg', 'Dew_Min',
                   'Hum_Max', 'Hum_Avg', 'Hum_Min',
                   'Win_Max', 'Win_Avg', 'Win_Min',
                   'Pre_Max', 'Pre_Avg', 'Pre_Min',
                   'Precipitation'
                   ]
    url = 'https://www.wunderground.com/history/monthly/us/ny/new-york-city/' \
          'KLGA/date/{:}'.format(date)
    browser.get(url)
    time.sleep(20)        # 使数据完整，否则可能缺少数据
    table = browser.find_element_by_xpath("//table[@class='days ng-star-inserted']")
    # tbody = table.find_element_by_tag_name('tbody')
    td_list = table.find_elements_by_xpath("tbody/tr/td")
    print(len(td_list))
    data_frame = []
    for td in td_list:
        column_list = []
        line_list = td.text.split('\n')
        line_list.pop(0)
        for line in line_list:
            column_list.append(line.split())
        data_frame.append(column_list)
    data_frame = np.concatenate(data_frame, axis=1)
    data_frame = pandas.DataFrame(data_frame, columns=column_name)
    data_frame.to_csv(save_path)
    # res = table.find_elements_by_xpath("//tbody")
    # print(res)
    browser.quit()


if __name__ == '__main__':
    craw_month_weather_data(2016, 1)
