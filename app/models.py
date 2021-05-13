from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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
    date = db.Column(db.DateTime, default=datetime.utcnow)
    started = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    section1 = db.Column(db.JSON)
    section2 = db.Column(db.JSON)
    section3 = db.Column(db.JSON)
    section4 = db.Column(db.JSON)
    section5 = db.Column(db.JSON)

    def __repr__(self):
        user = User.query.get(self.user_id)
        return f'<Quiz by {user.username} on {self.date}>'

    def get_associated_user(self):
        return User.query.get(self.user_id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Tutorial(db.Model):
    __tablename__ = 'tutorial'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    started = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    questions = db.Column(db.JSON)

    def __repr__(self):
        user = User.query.get(self.user_id)
        return f'<Tutorial by {user.username} on {self.date}>'

    def get_associated_user(self):
        return User.query.get(self.user_id)



