from flask import render_template, redirect, url_for, request
from flask_login import login_user, flash
import models
import code
from forms import Forms

def index():
    users = []
    for user in models.User.find():
        users.insert(0, user)
    return render_template('users/index.html', users=users)

def create():
    form = Forms.RegisterForm()
    
    if form.validate_on_submit():
        # login and validate the user...
        user = models.User.insert(form.user)
        login_user(user)
        flash("Logged in successfully.")
        return redirect("/")
    return render_template("login.html", form=form, type="register")

def quiz():
    """get a question from db present it, get a form feedback
    send back as a response to db, win"""
    question = None
    return render_template("quiz.html", question=question)