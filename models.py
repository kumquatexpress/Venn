from flask_login import UserMixin
import code

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

	@staticmethod
	def find(query={}):
		# processing here
		results = User.dbMap.find(query)
		if len(results) < 1:
			return None
		return map(lambda x: to_user(x), results)

	@staticmethod
	def find_one(query={}):
		user = User.dbMap.find_one(query)
		if user:
			return to_user(user)
		return None

	@staticmethod
	def insert(obj):
		# needs validation probably
		User.dbMap.insert(obj)
		return to_user(obj)

def to_user(obj):
	um = UserModel()
	um.id = obj['_id']
	um.data = obj
	return um

class UserModel(UserMixin):

	def init(self, *args, **kwargs):
		UserMixin.__init__(self, *args, **kwargs)


class Relationship(Model):
	pass

