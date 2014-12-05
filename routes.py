from flask import Blueprint, request
from flask_login import login_required
from handlers import main_handler, users_handler
from models import User
import code

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

@app.route("/facebook_auth", methods=["POST"])
def facebook_auth():
    return users_handler.facebook_create(request.json)

@app.route("/users")
@login_required
def index_users():
    return users_handler.index()

@app.route("/logout")
@login_required
def logout():
    return users_handler.logout()

@app.route("/quiz")
@login_required
def quiz():
    return users_handler.quiz()
