from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Question_Mark import db, app, login_manager
from flask_login import UserMixin
import flask_whooshalchemyplus as wa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    questions = db.relationship("Questions", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}', '{self.email}')"


class Questions(db.Model):
    __searchable__ = ["question"]
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    answers = db.relationship("Answers", backref="writer", lazy=True)

    def __repr__(self):
        return f"Questions('{self.question}', '{self.date_posted}')"


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(30), nullable=False
    )  ## Username of the user who answered the question
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quest_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)

    def __repr__(self):
        return f"Answers('{self.answer}', '{self.username}', '{self.date_posted}', '{self.quest_id}')"


wa.whoosh_index(app, Questions)
