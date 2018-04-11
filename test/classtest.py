class options_init():
	def __init__(self, users, province, city, age, gender, path, file):
		self.users = users
		self.province = province
		self.city = city
		self.age = age
		self.gender = gender
		self.path = path
		self.file = file

options = options_init(1,2,3,4,5,6,7)
#options = str(options)
print(type(options), options.__dict__)