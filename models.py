from flask_login import UserMixin
from collections import defaultdict
import code
import numpy as np

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

class Suggestion(object):

    def __init__(self, uid1, uid2):
        if uid1 > uid2:
            uid2, uid1 = uid1, uid2
        self.ua1, self.ua2 = User.find_one({"_id": uid1}), User.find_one({"_id": uid2})
        self.profile_rating = None
        self.user_rating = None
        self.total_rating = None
        self.valid = False

    def find_ratings(self):
        if self.ua1 is None or self.ua2 is None:
            return
        self.find_user_rating()
        self.find_profile_rating(self.ua1, self.ua2)
        if self.user_rating is None and self.profile_rating is None:
            return
        urate, prate = self.user_rating, self.profile_rating
        if urate is None:
        	urate = prate
        if prate is None:
        	prate = urate

        self.total_rating = (urate + prate)/float(2) * float(10)
        self.valid = True

    def find_user_rating(self):
        relationship = Relationship.find_one({"user1": str(self.ua1.data["_id"]),
            "user2": str(self.ua2.data["_id"])})
        if relationship is None:
            return None
        vals = relationship["answers"].values()
        if len(vals) > 0:
            self.user_rating = 10 - sum(vals)/float(len(vals))
        return None

    def find_profile_rating(self, ua1, ua2):
        answers1 = ua1.data.get("questions", defaultdict(int))
        answers2 = ua2.data.get("questions", defaultdict(int))
        keys = [k for k in answers1.keys() if k in answers2]

        try:
            answers1, answers2 = zip(*[(answers1[i],answers2[i]) for i in keys if answers1[i] > 0 and answers2[i] > 0])
            answers1 = list(answers1)
            answers2 = list(answers2)

            if len(answers1) > 0 and len(answers2) > 0:
                c = np.dot(answers1,np.transpose(answers2))/np.linalg.norm(answers1)/np.linalg.norm(answers2)
                self.profile_rating = (c + 1) * 50
        except:
            return None
