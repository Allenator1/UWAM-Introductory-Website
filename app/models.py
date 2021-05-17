from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableDict


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    preferred_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    tutorial = db.relationship('Tutorial', uselist=False, backref='user')
    submissions = db.relationship('Quiz', backref='user')
    current_quiz = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    finish_date = db.Column(db.DateTime)
    finance = db.Column(MutableDict.as_mutable(db.JSON), default={'Q' + str(i) : "" for i in range(1, 4)})
    marketing = db.Column(MutableDict.as_mutable(db.JSON), default={'Q' + str(i) : "" for i in range(1, 4)})
    chassis = db.Column(MutableDict.as_mutable(db.JSON), default={'Q' + str(i) : "" for i in range(1, 4)})
    vehicle_dynamics = db.Column(MutableDict.as_mutable(db.JSON), default={'Q' + str(i) : "" for i in range(1, 4)})
    powertrain = db.Column(MutableDict.as_mutable(db.JSON), default={'Q' + str(i) : "" for i in range(1, 4)})

    def __repr__(self):
        user = User.query.get(self.user_id)
        return f'<Quiz by {user.username} on {self.start_date}>'


class Tutorial(db.Model):
    __tablename__ = 'tutorial'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.Column(MutableDict.as_mutable(db.JSON), default={'Q' + str(i) : "" for i in range(1, 11)})

    def __repr__(self):
        user = User.query.get(self.user_id)
        return f'<Tutorial for {user.username}>'

    def new_tutorial(self):
        self.questions = {'Q' + i : "" for i in range(1, 11)}


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



