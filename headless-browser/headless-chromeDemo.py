# -*- coding: utf-8 -*-

# 演示 selenium 以无头模式打开chrome

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'http://www.ivsky.com/tupian/'

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

print(driver.page_source)

driver.close()