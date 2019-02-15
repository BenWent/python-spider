import requests
from lxml import etree

from datetime import datetime
import json

import matplotlib.pyplot as plt

## 分析红楼梦的评分信息

class RemarkInfo:
	def __init__(self, rank, date, count):
		# 参数依次为 的分数区间、发布评论的时间、同样的信息（相同的年份、相同的评分）
		# 出现的次数
		self.rank = rank
		self.date = date

		self.count = count

	def __eq__(self, other):
		self_year = int(
				datetime.strptime(self.date, '%Y-%m-%d') \
					.timetuple().tm_year
			)
		other_year = int(
				datetime.strptime(other.date, '%Y-%m-%d') \
					.timetuple().tm_year
			)

		return self.rank == other.rank and self_year == other_year

	def __str__(self):
		return '[%s, %s, %s]' %(self.rank, self.date, self.count)

# 将 RemarkInfo对象 转换为 dict对象
def remarkInfoToDict(remark_info):
	return {
		'rank': remark_info.rank,
		'date': remark_info.date,
		'count': remark_info.count
	}


# 将 dict对象 转换为 RemarkInfo对象
def dictToRemarkInfo(remarkInfoDict):
	return Person(remarkInfoDict['rank'], remarkInfoDict['date'], \
		remarkInfoDict['count'])

if __name__ == '__main__':
	# 待分数数据集
	remark_info_list = []

	try:# 尝试读取 remark_info.json文件 是否存在。
		with open('remark_info.json', 'r') as fp:
			# 存在，直接使用里面的json数据，
			remark_info_list = json.load(fp, object_hook=dictToRemarkInfo)
	except FileNotFoundError: # 不存在，爬取数据
		base_url = 'https://book.douban.com/subject/1007305/comments/hot?p=%s'

		# 获取总的评论数
		resp = requests.get(base_url % (1))
		html = etree.HTML(resp.text)
		total_comments_text = html \
			.xpath('//span[@id="total-comments"]/text()')[0]
		total_comments_num = int(total_comments_text.replace('全部共', '') \
			.replace('条', '').strip())
		# 计算总的评论数被分为多少页显示
		page_num = total_comments_num // 20
		if total_comments_num % 20 != 0:
			page_num += 1

		# 开始获取书评信息
		for i in range(1, page_num + 1):
			# //*[@id="comments"]/ul/li[13]/div[2]/h3/span[2]/span[1]
			# //*[@id="comments"]/ul/li[13]/div[2]/h3/span[2]/span[2]
			# //*[@id="comments"]/ul/li[12]/div[2]/h3/span[2]/span
			//*[@id="comments"]/div[9]/div[2]/h3/span[2]/span[3]
			info_resp = requests.get(base_url % i)
			info_html = etree.HTML(info_resp.text)
			# 请求数据
			info_li_list = info_html.xpath('//*[@id="comments"]/ul/li')

			if len(info_li_list) == 0: # ip可能已经被封，不再请求数据
				break

			# 解析网页数据
			for info_li in info_li_list:
				info_span_list = info_li.xpath('div[2]/h3/span[2]/span')
				if len(info_span_list) == 2:
					info_rank = int(info_span_list[0].xpath('@class')[0] \
						.split(' ')[0] \
						.replace('allstar', '')) // 10
					info_date = info_span_list[1].xpath('text()')[0].strip()

					remark_info = RemarkInfo(info_rank, info_date, 0)
					try:
						index = remark_info_list.index(remark_info)
						remark_info_list[index].count += 1
					except ValueError as ve:
						remark_info_list.append(remark_info)

		# 将爬取的数据序列化到 remark_info.json文件 中
		with open('remark_info.json', 'w') as fp:
			json.dump(remark_info_list, fp, default=remarkInfoDict)


	# 绘图分析

	## 1、按分数统计
	ranks = (i for i in range(1, 6)) # 1star 至于 5star
	counts = [0 for i in range(len(ranks) + 1)]

	# 统计
	for remark_info in remark_info_list:
		counts[remark_info.rank] += 1
	# 删除 counts的第一个元素
	del counts[0]

	# 直方图
	plt.bar(ranks, counts, align='center', color='purple', alpha=0.8)
	plt.xlabel('star-number')
	plt.ylabel('people-number')
	plt.title('A Dream in Red Mansions')

	for x, y in enumerate(counts):
		plt.text(x, y+200, '%s' %round(y, 1), ha='center', va='baseline')

	plt.show()


