import requests
import re

base_url = "http://tieba.baidu.com/"#百度贴吧地址

resp = requests.get(base_url + "/f?kw=bilibili")#爬取百度贴吧的那个主题

pattern = re.compile(r'<a rel="noreferrer"\s*href="([\w/]+)"')#搜集主题第一页的所有url的正则表达式

url_list = pattern.findall(resp.text)#搜集主题第一页的所有url

img_pattern = re.compile(r'<img class="BDE_Image".+src="(.+jpg)"')#爬取每个节点下的图片
img_name_pattern = re.compile(r"/+")#获取爬取图片的名字
while len(url_list) != 0:#遍历第一页的所有url
    current_url = base_url + url_list.pop()
    current_resp = requests.get(current_url)
    img_list = img_pattern.findall(current_resp.text)
    while len(img_list) != 0:
        current_img_url = img_list.pop()
        img_name = img_name_pattern.split(current_img_url).pop()
        img_resp = requests.get(current_img_url)

        with open("E:/imgs/" + img_name,"wb") as file:
            file.write(img_resp.content)