import requests
from lxml import etree

from openpyxl import Workbook
from datetime import datetime

## 爬取ip138网站上的邮政编码和长途区号等信息，并把它写入到excel文件中

if __name__ == '__main__':
	base_url = 'http://www.ip138.com'
	encoding = 'gb2312'
	# 创建一个Excel文件
	wb = Workbook() 

	response = requests.get(base_url + '/post/')
	response.encoding = encoding
	html = etree.HTML(response.text)

	# 得到 全国邮编区号大全 表格
	post_table = html.xpath('//div[@id="newAlexa"]')
	# 获取表格下的所有 a 标签
	post_a_list = post_table[0].xpath('table//a')
	for post_a in post_a_list:
		# 获取每个省份的编号
		post_province_num = post_a.xpath('@href')[0]
		# 获取每个省份的名字
		post_province_name = post_a.xpath('text()')[0]

		# 跳转到每个省份页面
		province_page_response = requests.get(base_url + post_province_num)
		province_page_response.encoding = encoding
		province_page_html = etree.HTML(province_page_response.text)

		# 获取每个省份下每个市、县、区的邮编
		province_table_row_list = province_page_html \
			.xpath('//tr[@bgcolor="#ffffff"]')

		# 为Excel文件创建每个省份的sheet
		province_sheet = wb.create_sheet(post_province_name)
		province_sheet.append(['市、县、区', '邮政编码', '长途区号'])

		# print(post_province_name)

		pre_county_name = ""
		for province_table_row in province_table_row_list:
			county_cols = province_table_row.xpath('td')

			for i in range(len(county_cols) // 3):
				aLabel = county_cols[i * 3].xpath('a')
				if len(aLabel) != 0: # <td> 下没有a标签
					pre_county_name = aLabel[0].xpath('b/text()')[0]
				else: # <td> 下有a标签
					county_name = county_cols[i * 3].xpath('text()')[0]
					if county_name != '\xa0': 
						# <td> 的内容不是 &nbsp;
						county_post = county_cols[i * 3 + 1] \
							.xpath('a/text()')[0]
						county_area_code = county_cols[i * 3 + 2] \
							.xpath('a/text()')[0]

						if(pre_county_name != ''):
							county_name = '%s - %s' % (pre_county_name, \
								county_name)

						province_sheet.append([ \
							county_name.encode('utf-8'), \
							county_post.encode('utf-8'), \
							county_area_code.encode('utf-8') \
							])
			
	#删除默认创建的sheet
	wb.remove_sheet(wb.get_sheet_by_name('Sheet'))
	# 保存Excel文件
	wb.save('全国邮编区号大全.xlsx')