from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    primary_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    preferred_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    submissions = db.relationship('Quiz', backref='user', lazy=True)
    tutorial = db.relationship('Tutorial', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Quiz(db.Model):
    primary_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.primary_id'), nullable=False)


class Tutorial(db.Model):
    primary_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.primary_id'), nullable=False)