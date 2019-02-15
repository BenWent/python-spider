import json

# 将对象直接变为json字符串写入到文件中

class Person:
	def __init__(self, name, gender):
		self.name = name
		self.gender = gender


def toDict(person):
	return{
		'name': person.name,
		'gender': person.gender
	}


if __name__ == '__main__':
	peroson_list = [Person('leo', 'male'),Person('lili', 'female')]
	# json能直接将 list 转换为json数组
	with open('person_list.json', 'w+') as fp:
		json.dump(peroson_list, fp, default=toDict)
