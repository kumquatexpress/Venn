from flask import Blueprint
from handlers import main_handler

app = Blueprint('app', __name__, template_folder='templates')

@app.route("/")
def main_page():
    return main_handler.index()
