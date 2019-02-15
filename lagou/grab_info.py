#Author:Went
# -*- coding:utf-8 -*-
#该脚本的作用是抓取拉钩网的职位、工资等信息
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os
import json
import time
import re
from openpyxl import workbook

base_url = "https://www.lagou.com"

chrome_options = Options()
chrome_options.add_argument("--headless")#使Chrome变为无头模式
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get(base_url)

'''
给此次请求添加cookie
'''
with open(os.getcwd() + "/main_page_cookies.json","r") as file:
    cookies = json.load(file)
for cookie in cookies:
    browser.add_cookie({
        'domain':cookie['domain'],
        'path':cookie['path'],
        'name':cookie['name'],
        'value':cookie['value']
    })
browser.get(base_url)

search_input = browser.find_element_by_id("search_input")#获得搜索框
key_words = input("输入关键字搜索：")#键入搜索关键字
search_input.send_keys(key_words)
search_input.send_keys(Keys.ENTER)

current_url = browser.current_url#关键词搜索后的主页面

'''
正则表达式
'''
company_pattern = re.compile(r'<li.*data-company="(.*)"\s+data-positionname')
position_pattern = re.compile(r"<h3.*>(.*)</h3>")
location_pattern = re.compile(r"<em>(.*)</em>")
salary_pattern = re.compile(r'<span\s+class="money">(.+)</span>')
experience_pattern = re.compile(r"<!--<i></i>-->(.*)\s+")
# details_url_pattern = re.compile(r'<a\s+class="position_link"\s+href="(.*)"\s+target.*>')

wb = workbook.Workbook()
ws = wb.active#建立一个Excel表格

ws.append(['公司','职位','地址','工资','经验'])
while True:
    time.sleep(0.5)#浏览器解析JavaScript获得可见的页面

    companies = company_pattern.findall(browser.page_source)
    positions = position_pattern.findall(browser.page_source)
    locations = location_pattern.findall(browser.page_source)
    salaries = salary_pattern.findall(browser.page_source)
    experiences = experience_pattern.findall(browser.page_source)
    # details = details_url_pattern.findall(browser.page_source)

    '''
    将数据写入到Excel中
    '''
    for index,company in enumerate(companies):
        ws.append([company,positions[index],locations[index],salaries[index],experiences[index]])

    try:
        next_button = browser.find_element_by_class_name("pager_next")#可能存在职位太少，不用分页
        next_button.click()
    except:
        break
    try:
        if browser.find_element_by_class_name("pager_next_disabled"):
            break
    except NoSuchElementException as nsee:
        pass


wb.save(key_words + ".xlsx")
wb.close()
browser.close()

# print(browser.page_source)

