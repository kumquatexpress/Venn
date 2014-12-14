from flask import render_template, redirect, url_for, request, make_response
from flask_login import login_user, flash, logout_user, current_user
import models
import code
import random
from forms import Forms

PROB = 5 # random(0, 10) < this means generate user -> user question, < 0 means never generate
LENGTH = 8
RETRIES = 6

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
    form = Forms.QuizForm()
    qid = select_question(current_user)
    question = models.Question.find_one({"question_id": qid})
    rel = False
    worked = True

    if qid is None or random.randint(0, 10) < PROB:
        rel = True
        users = get_user_pair(current_user)
        for i in range(RETRIES):
            if users is None:
                users = get_user_pair(current_user)
            else:
                break

        if users is None:
            worked = False
        else:
            user1, user2 = users
            question = make_relationship_question(user1, user2)

    if form.validate_on_submit():
        # login and validate the user...
        if form.question_id is None:
            code.interact(local=locals())
            r = models.Relationship.find_one({"user1": form.userid1, "user2": form.userid2})
            if r is None:
                r = {
                    "user1": form.userid1,
                    "user2": form.userid2,
                    "answers": {}
                }
            r["answers"][str(current_user.data["_id"])] = form.answer
            code.interact(local=locals())
            models.Relationship.update(r)
        else:
            current_user.data["questions"] = current_user.data.get("questions", {})
            current_user.data["questions"][str(form.question_id)] = form.answer

            models.User.update(current_user.data)

        return redirect("/quiz")
    if worked:
        return render_template("quiz.html", form=form, question=question, relationship=rel)
    else:
        return redirect("/quiz")

def logout():
    logout_user()
    return redirect("/")

def select_question(user):
    answered = user.data.get("questions", [])
    questions = models.Question.find()
    idx = range(1, questions.count())
    random.shuffle(idx)
    for q in idx:
        if str(int(questions[q]["question_id"])) not in answered:
            return q
    return None

def get_user_pair(user):
    users = models.User.find({"_id": {"$ne": current_user.data["_id"]}})
    if len(users) < 2:
        return None
    id1, id2 = random.randint(0, len(users)-1), random.randint(0, len(users)-1)
    if id1 == id2:
        return None
    r = models.Relationship.find_one({"user1": users[id1].data["_id"], "user2": users[id2].data["_id"]})
    if r is not None:
        if current_user.data["_id"] in r["answers"]:
            return None
    return (users[id1].data, users[id2].data)

def make_relationship_question(u1, u2):
    ret_question = {}
    ret_question["title"] = "How compatible are these two users?"
    ret_question["text"] = "Based on their answers to the questions below, how well do you think these two users would get along?"
    ret_question["user1"] = u1["username"]
    ret_question["user2"] = u2["username"]
    ret_question["userid1"] = u1["_id"]
    ret_question["userid2"] = u2["_id"]

    intersect = [qid for qid in u1["questions"].keys() if qid in u2["questions"].keys()]
    u1_difference = [qid for qid in u1["questions"].keys() if qid not in u2["questions"].keys()]
    u2_difference = [qid for qid in u2["questions"].keys() if qid not in u1["questions"].keys()]
    random.shuffle(intersect)
    random.shuffle(u2_difference)
    random.shuffle(u1_difference)
    
    ret_question["answers"] = []
    for i in intersect[:LENGTH]:
        question = models.Question.find_one({"question_id": int(i)})
        if question is not None:
            ret_question["answers"].append({
                "image": question["image"],
                "user1": u1["questions"][i],
                "user2": u2["questions"][i]
            })

    if len(ret_question["answers"]) < LENGTH:
        for i in range((LENGTH - len(ret_question["answers"]))/2):
            if len(u1_difference) > i:
                qid = u1_difference[i]
                if qid is not None:
                    question = models.Question.find_one({"question_id": int(qid)})
                    if question is not None:
                        ret_question["answers"].append({
                            "image": question["image"],
                            "user1": u1["questions"][qid],
                            "user2": "Not answered"
                        })

            if len(u2_difference) > i:
                qid = u2_difference[i]
                if qid is not None:
                    question = models.Question.find_one({"question_id": int(qid)})
                    if question is not None:
                        ret_question["answers"].append({
                            "image": question["image"],
                            "user1": "Not answered",
                            "user2": u2["questions"][qid]
                        })
    return ret_question
