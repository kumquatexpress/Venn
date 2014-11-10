class Question(object):
	dbMap = None

	@staticmethod
	def initialize_db(conn):
		Question.dbMap = conn.questions

	@staticmethod
	def find_one(query={}):
		return Question.dbMap.find_one(query)

	@staticmethod
	def find(query={}):
		# processing here
		return Question.dbMap.find(query)

	@staticmethod
	def insert(obj):
		# needs validation probably
		return Question.dbMap.insert(obj)

class User(object):
	dbMap = None

	@staticmethod
	def initialize_db(conn):
		User.dbMap = conn.users

	@staticmethod
	def find_one(query={}):
		return User.dbMap.find_one(query)

	@staticmethod
	def find(query={}):
		# processing here
		return User.dbMap.find(query)

	@staticmethod
	def insert(obj):
		# needs validation probably
		return User.dbMap.insert(obj)
