#Author:Went
# -*- coding:utf-8 -*-
import requests
import time

params = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
}
resp = requests.get("https://www.lagou.com/jobs/3024351.html",params=params)
resp.encoding = "utf-8"
time.sleep(5)
print(resp.text)
