# -*- coding: utf-8 -*-

# 抓取图片，参考：https://www.jianshu.com/p/11e0c8c88cdb

from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import pyautogui


url = 'http://www.ivsky.com/tupian/'

driver = webdriver.Chrome()
driver.get(url)

for img in driver.find_elements_by_tag_name('img'):
	print(img.get_attribute('src'))
	try:
		# 将光标移动到元素上, 点击鼠标右键, 点击键盘向下键，使页面向下滚动
		ActionChains(driver) \
		 .move_to_element(img) \
		 .context_click(img) \
		 .perform()

		# 无法按下 V 键：https://blog.csdn.net/jasonwang_/article/details/83217421
		# actions.send_keys('V') 
		# actions.send_keys(Keys.ENTER)

		# pyautogui.typewrite(['v', 'enter'])
		pyautogui.typewrite(['V'])
		time.sleep(1)
		pyautogui.press(['enter'])
		pyautogui.press('down')
	except BaseException as be:
		continue

driver.close()

# PyAutoGUI 简介:
#	 https://www.cnblogs.com/dcb3688/p/4607980.html
# 安装： pip install PyAutoGUI==0.9.33