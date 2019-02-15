import json

# 将文件中的json字符串转换为自定义对象

class Person:
	def __init__(self, name, gender):
		self.name = name
		self.gender = gender

	def __str__(self):
		return '[%s, %s]' %(self.name, self.gender)


def jsonToPerson(personDict):
	return Person(personDict['name'], personDict['gender'])

if __name__ == '__main__':
	with open('person_list.json', 'r') as fp:
		# json.load将读取到的json集合的每个元素送给 函数jsonToPerson 进行解析
		person_list = json.load(fp, object_hook=jsonToPerson)
		for person in person_list:
			print(person)