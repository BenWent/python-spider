from lxml import etree

### 探究如何使用lxml

text = '''
	<table id='testId'>
		<tr>
			<td>hello,world</td>
			<td>
				<a href='link'>link</a>
			</td>
		</tr>
		<tr>
			<td>hello,world</td>
			<td>
				hello,python
			</td>
			<td>&nbsp;</td>
		</tr>
	</table>
'''

html = etree.HTML(text) # 会自动对html代码进行补全，即添加<html>、<body>
						# 等必要标签，参考：
						# https://www.cnblogs.com/zhangxinqi/p/9210211.html
# print(etree.tostring(html))

tr_list = html.xpath('//table[@id="testId"]//tr')


###错误写法
# tr_list = html.xpath('table[@id="testId"]//tr')

for tr in tr_list:
	td_list = tr.xpath('td')
	for td in td_list:
		if len(td.xpath('a')) != 0:
			print('a标签的内容为', td.xpath('a/text()')[0])
		else:
			# 一个 &nbsp;相当于一个 \xa0
			if(td.xpath('normalize-space(text())') == '\xa0'):
				print('------')
			else:
				print('td下没有a标签, td的内容为', \
					td.xpath('normalize-space(text())'))
