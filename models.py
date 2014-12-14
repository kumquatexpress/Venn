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
	def find(query={}, limit=0):
		# processing here
		return Question.dbMap.find(query).limit(limit)

	@staticmethod
	def insert(obj):
		# needs validation probably
		return Question.dbMap.insert(obj)

	@staticmethod
	def count():
		return User.dbMap.count()

class Question(Model):

	@staticmethod
	def initialize_db(conn):
		Question.dbMap = conn.questions

class User(Model):

	@staticmethod
	def initialize_db(conn):
		User.dbMap = conn.users

	@staticmethod
	def find(query={}, limit=0):
		# processing here
		results = User.dbMap.find(query).limit(limit)
		if results.count() < 1:
			return None
		return map(lambda x: to_user(x), [r for r in results])

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

	@staticmethod
	def update(obj):
		# needs validation probably
		User.dbMap.save(obj)
		return to_user(obj)

	@staticmethod
	def count():
		return User.dbMap.count()

def to_user(obj):
	um = UserModel()
	um.id = obj['_id']
	um.data = obj
	return um

class UserModel(UserMixin):

	def init(self, *args, **kwargs):
		UserMixin.__init__(self, *args, **kwargs)
		self.data = None

	def is_authenticated(self):
		return self.data is not None

class Relationship(Model):
	
	@staticmethod
	def initialize_db(conn):
		Relationship.dbMap = conn.relationships

	@staticmethod
	def find(query={}, limit=0):
		Relationsip.dbMap = conn.relationships
		# processing here
		results = Relationship.dbMap.find(query).limit(limit)
		if results.count() < 1:
			return None
		return results

	@staticmethod
	def find_one(query={}):
		return Relationship.dbMap.find_one(query)

	@staticmethod
	def insert(obj):
		# needs validation probably
		return Relationship.dbMap.insert(obj)

	@staticmethod
	def update(obj):
		# needs validation probably
		return Relationship.dbMap.save(obj)
		
	@staticmethod
	def count():
		return Relationship.dbMap.count()

