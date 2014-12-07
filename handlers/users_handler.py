from flask import render_template, redirect, url_for, request, make_response
from flask_login import login_user, flash, logout_user, current_user
import models
import code
import random
from forms import Forms

PROB = -1 # random(0, 10) < this means generate user -> user question, < 0 means never generate

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

def facebook_create(info):
    user = models.User.find_one({"facebook_uid": info["id"]})
    if user is None:
        user = models.User.insert({
            "facebook_uid": info["id"],
            "username": info["name"],
            "gender": info["gender"]
        })
    if user is None:
        return make_response(("Failed to create a user", 500, []))
    login_user(user)
    return make_response(("Logged in successfully", 200, []))

def quiz():
    """get a question from db present it, get a form feedback
    send back as a response to db, win"""
    qid = select_question(current_user)
    question = models.Question.find_one({"question_id": qid})
    if qid is None or random.randint(0, 10) < PROB:
        try:
            user1, user2 = get_user_pair(current_user)
        except TypeError:
            return redirect("/quiz", alert="Oops, it seems we ran out of questions.")

    form = Forms.QuizForm()

    if form.validate_on_submit():
        # login and validate the user...
        current_user.data["questions"] = current_user.data.get("questions", {})
        current_user.data["questions"][str(form.question_id)] = form.answer

        models.User.update(current_user.data)
        return redirect("/quiz")
    return render_template("quiz.html", form=form, question=question)

def logout():
    logout_user()
    return redirect("/")

def select_question(user):
    answered = user.data.get("questions", [])
    questions = models.Question.find()
    idx = range(1, questions.count())
    random.shuffle(idx)
    for q in idx:
        if questions[q]["question_id"] not in answered:
            return q
    return None

def get_user_pair(user):
    users = models.User.find()
    if len(users) < 2:
        return None
    id1, id2 = random(0, models.User.count()-1), random(0, models.User.count()-1)
    if id1 == id2:
        return get_user_pair(user)
    return (users[id1], users[id2])
