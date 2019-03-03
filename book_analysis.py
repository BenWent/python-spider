import requests
from lxml import etree

from datetime import datetime
import json

from functools import reduce
import pylab as plt

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
	return RemarkInfo(remarkInfoDict['rank'], remarkInfoDict['date'], \
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
			# //*[@id="comments"]/div[9]/div[2]/h3/span[2]/span[3]
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
						.split(' ')[1] \
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
			json.dump(remark_info_list, fp, default=remarkInfoToDict)


	# 绘图分析

	## 1、按分数统计
	ranks = [i for i in range(1, 6)] # 1star 至于 5star
	counts = [0 for i in range(len(ranks) + 1)]
	## 2、按年份统计
	star_dict_group_by_year = {}

	# 统计
	for remark_info in remark_info_list:
		counts[remark_info.rank] += remark_info.count

		if remark_info.rank == 5: # 只统计5-star
			star_dict_group_by_year[int(
				datetime.strptime(remark_info.date, '%Y-%m-%d') \
					.timetuple().tm_year
			)] = remark_info.count

	# 删除 counts的第一个元素
	del counts[0]

	# 直方图
	plt.figure(1)

	plt.subplot(121)
	plt.bar(ranks, counts, align='center', color='purple', alpha=0.8)
	plt.xlabel('star-number')
	plt.ylabel('people-number')
	plt.title('A Dream in Red Mansions')
	for x, y in enumerate(counts):
		plt.text(x+1, y+20, '%s' %(y), ha='center', va='baseline')

	# 按年份统计 5-star，绘制饼状图
	# 处理数据
	years = []
	nums = []
	for key, value in sorted(star_dict_group_by_year.items(), reverse=True):
		years.append(key)
		nums.append(value)

	percentage_nums = list(map(lambda x, y: round(x/y, 4), nums, 
		(reduce(lambda x, y: x+y, nums) 
			for i in range(len(nums)))
		))

	explode = [0 for i in range(len(years))]
	explode[0] = 0.2 # 突出显示最新年份的数据
	explode[nums.index(max(nums))] = 0.2 # 突出显示评价最高的年份

	# for x, y, z in zip(years, nums, percentage_nums):
	# 	print(x, y, z)

	# 绘制按年份5-star统计的直方图
	plt.subplot(122)
	plt.bar(years, nums, align='center', color='purple', alpha=0.8)
	plt.xlabel('year')
	plt.ylabel('5star-number')
	plt.title('A Dream in Red Mansions')
	for x, y in zip(years, nums):
		plt.text(x, y+20, '%s' %(y), ha='center', va='baseline')

	# 绘制按年份5-star统计的饼状图
	plt.figure(2)
	plt.style.use('ggplot')
	plt.xlim(0, 1)
	plt.ylim(0, 1)
	plt.axes(aspect='equal')
	plt.pie(x=percentage_nums, # 百分比数据
		labels=years, # 文字标签
		explode=explode, # 突出显示某部分数据
		pctdistance=0.8, # 设置百分比标签与圆心的距离
		labeldistance=1.15, # 设置文字标签与圆心的距离
		autopct='%.2f%%', # 设置百分比保留两位小数
	) 

	plt.show()


# 从最终的图标中可以看出
## 1、对《红楼梦》的关注主要开始与2007，到2012年达到最高峰，但从2013开始关注度开始
## 降温