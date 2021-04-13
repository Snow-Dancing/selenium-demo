# 爬取美国纽约历史天气 (zcz)

>#### 基本说明

* 需要安装 selenium 和 pandas 库

* 在[此处](http://chromedriver.storage.googleapis.com/index.html)下载合适的 chrome 驱动，并放在 python.exe 所在目录下

* 我已在本目录下提供了一个89版本的驱动： chromedriver.exe

* 天气数据原始网址在[此处](https://www.wunderground.com/history/daily/us/ny/new-york-city)  


>#### 使用方法

* craw_day.py 针对每天数据进行爬取，结果保存在 day_csv 文件夹下

* craw_month.py 针对每个月的汇总数据进行爬取，结果保存在 month_csv 文件夹下

