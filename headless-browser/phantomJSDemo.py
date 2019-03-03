from selenium import webdriver

# 创建PhantomJS对象，PhantomJS需要配置环境变量
driver = webdriver.PhantomJS()
driver.set_window_size(1366, 768)

url = 'https://www.baidu.com'

driver.get(url)

driver.save_screenshot('%s.png' % driver.title)

driver.close()