import requests
from lxml import etree

## 爬取豆瓣top250的书籍，并根据算法 得分*评论人数 打印出最终前top-10的书籍信息

class Book:
	def __init__(self, name, author, critic_num, rank):
		# 参数依次表示为：书名、书作者、评论家人数、得分数
		self.name = name
		self.author = author
		self.critic_num = int(critic_num)
		self.rank = float(rank)

		self.score = self.critic_num * self.rank


	@classmethod
	def from_book_table_row(cls, book_table_row):

		name = book_table_row \
			.xpath('td[2]/div[1]/a/@title')[0]

		author = book_table_row.xpath('td[2]/p/text()')[0]
		author = author[0:author.index('/')]

		critic_num = book_table_row \
			.xpath('td[2]/div[2]/span[3]/text()')[0]
		critic_num = \
			critic_num[critic_num.index('(') + 1: \
				critic_num.rindex(')')].strip()
		critic_num = critic_num[0: critic_num.rindex('人')]


		rank = book_table_row.xpath('td[2]/div[2]/span[2]/text()')[0]

		return cls(name, author, critic_num, rank)

	def __le__(self, other):
		return self <= other.score

	def __lt__(self, other):
		return self.score < other.score

	def __ge__(self, other):
		return self.score >= other.score

	def __gt__(self, other):
		return self.score > other.score

	def __str__(self):
		return "%s, %s, %s, %s" \
			%(self.name, self.author, self.critic_num, self.rank)


if __name__ == '__main__':
	base_url = 'https://book.douban.com/top250?start=%s'

	with open('豆瓣top250.txt', 'w+', encoding='utf-8') as fb:
		fb.write('著作名\t\t作者\t\t评论数\t\t得分\n')

	# 排名前10的书籍列表
	top_10_book_list = []
	for i in range(0, 226, 25):
		resp = requests.get(base_url % (i))
		html = etree.HTML(resp.text)

		book_table_row_list = html.xpath('//tr[@class="item"]')

		# 将数据写入到文件
		for book_table_row in book_table_row_list:
			book = Book.from_book_table_row(book_table_row)
			# print(book)

			if len(top_10_book_list) < 10:
				top_10_book_list.append(book)
			else:
				top_10_book_list.sort(reverse=True)
				if top_10_book_list[-1] < book:
					top_10_book_list[-1] = book

			with open('豆瓣top250.txt', 'a+', encoding='utf-8') as fb:
				fb.write( \
					'{_name}\t{_author}\t{_critic_num}\t{_rank}\n' \
					.format(_name=book.name, _author=book.author, \
						_critic_num=book.critic_num, _rank=book.rank))

	# 打印出前10的书籍
	top_10_book_list.sort(reverse=True)
	for book in top_10_book_list:
		print(book)