from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from app.models import User
from app.models import Quiz


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me!')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
        Regexp("[[a-zA-Z\_\d]{2,32}")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    preferred_name = StringField('Preferred Name')
    password = StringField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), 
        EqualTo(password)])
    remember_me = BooleanField('Remember Me!')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken')

    def validate_email(self, email):
        if email.data:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email already has a registered account')