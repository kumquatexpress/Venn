from flask import Blueprint
from flask_login import login_required
from handlers import main_handler, users_handler
from models import User

app = Blueprint('app', __name__, template_folder='templates')

@app.route("/")
def main_page():
    return main_handler.index()

@app.route("/login", methods=["GET", "POST"])
def login():
    return main_handler.login()

@app.route("/register", methods=["GET", "POST"])
def register():
    return users_handler.create()

@app.route("/users")
@login_required
def index_users():
    return users_handler.index()

@app.route("/quiz")
@login_required
def quiz():
    return users_handler.quiz()
