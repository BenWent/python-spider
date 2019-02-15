# 探究 in 的实现原理：
## 遍历 可迭代对象 与 待判断对象 使用 == 符号进行判断

class Person:
	def __init__(self, name, gender):
		self.name = name
		self.gender = gender

	def __eq__(self, other):
		return self.name == other.name and self.gender == other.gender

	def __str__(self):
		return '[%s, %s]' %(self.name, self.gender)

if __name__ == '__main__':
	# 可迭代对象
	person_list = [Person('kity', 'male'), Person('kitty', 'male')]

	# 待判断对象
	p1 = Person('kitty', 'male') 
	p2 = Person('mitty', 'male')

	if p1 in person_list: # 实质是使用 len(person_list) 次 == 进行判断
		print(p1, '存在', '位置为:', person_list.index(p1) + 1)
	else:
		print(p1, '不存在')

	print(person_list.index(p2))
	if p2 in person_list: # 实质是使用 len(person_list) 次 == 进行判断
		print(p2, '存在', '位置为:', person_list.index(p2) + 1)
	else:
		print(p2, '不存在')