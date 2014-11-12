from flask import Blueprint
from handlers import main_handler, users_handler
from models import User

app = Blueprint('app', __name__, template_folder='templates')

@app.route("/")
def main_page():
    return main_handler.index()

@app.route("/users")
def index_users():
    return users_handler.index()
