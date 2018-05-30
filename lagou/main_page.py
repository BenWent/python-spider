#Author:Went
# -*- coding:utf-8 -*-
#该脚本的作用是搜集拉钩网首页的cookies

from selenium import webdriver
import json
import os

browser = webdriver.Chrome()
browser.get("https://www.lagou.com")

with open(os.getcwd() + "/main_page_cookies.json","w") as file:
    json.dump(browser.get_cookies(),file)
# print(browser.current_url)
browser.close()
