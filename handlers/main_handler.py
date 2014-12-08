from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user
import models
from forms import Forms
import code

def index():
    return render_template('index.html')

def login():
    form = Forms.LoginForm()
    
    if form.validate_on_submit():
        # login and validate the user...
        login_user(form.user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or "/")
    return render_template("login.html", form=form)