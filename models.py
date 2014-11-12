class Model(object):
	dbMap = None

	@staticmethod
	def initialize_db(conn):
		pass

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

class Question(Model):

	@staticmethod
	def initialize_db(conn):
		Question.dbMap = conn.questions

class User(Model):

	@staticmethod
	def initialize_db(conn):
		User.dbMap = conn.users

class Relationship(Model):
	pass

