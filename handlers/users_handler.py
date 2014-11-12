from flask import render_template
import models
import code

def index():
    users = []
    for user in models.User.find():
        users.insert(0, user)
    return render_template('users/index.html', users=users)