import random
from datetime import date
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login&register.html', type='Login', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        if not form.preferred_name.data:
            user.preferred_name = user.username
        else:
            user.preferred_name = form.preferred_name.data
        if form.email.data:
            user.email = form.email.data
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Added the user: {user.username}')
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login&register.html', type="Register", form=form)

