from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField
from flask_wtf.html5 import IntegerRangeField
import models
import code

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = models.User.find_one({"username": self.username.data})
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not check_password(user.data["password"], self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if len(self.username.data) < 1:
            self.username.errors.append('Unknown username')
            return False

        if len(self.password.data) < 3:
            self.password.errors.append('Invalid password')
            return False

        self.user = {"username": self.username.data, "password": self.password.data}
        return True

class QuizForm(Form):

    ans = IntegerRangeField('Answer', [validators.Required()])
    qid = HiddenField('QuestionId', [validators.Required()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)
        self.answer = None
        self.question_id = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        
        self.answer = self.ans.data
        self.question_id = int(float(self.qid.data))
        return True

def check_password(p1, p2):
    return p1 == p2