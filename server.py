from routes import app
from flask import Flask, current_app
from flask.ext.pymongo import PyMongo
import code
from models import User, Question

main_app = Flask(__name__)
main_app.register_blueprint(app)

mongo = PyMongo(main_app)

with main_app.app_context():	
	User.initialize_db(mongo.db)
	Question.initialize_db(mongo.db)

User.insert({"name": "hellotest"})

if __name__ == "__main__":
    main_app.run()