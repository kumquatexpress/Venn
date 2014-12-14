from routes import app
from flask import Flask, current_app
from flask.ext.pymongo import PyMongo, ObjectId
import code
from flask_login import *
from models import User, Question, Relationship
import yaml

db = yaml.load(open("config/db.yaml"))

main_app = Flask(__name__)
main_app.register_blueprint(app)
main_app.secret_key = db['secret']
main_app.config['MONGO_DBNAME'] = "venn_development"
main_app.config['MONGO_URI'] = db["uri"]

mongo = PyMongo(main_app)

login_manager = LoginManager()

login_manager.setup_app(main_app)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(userid):
    return User.find_one({'_id':ObjectId(userid)})

with main_app.app_context():
    User.initialize_db(mongo.db)
    Question.initialize_db(mongo.db)
    Relationship.initialize_db(mongo.db)

if __name__ == '__main__':
    main_app.run(debug=True)