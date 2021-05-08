import random
from datetime import date
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        next_page = request.args.get('next')
        login_user(user, remember=form.remember_me.data)
        if not next_page:
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login&register.html', type='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        if not form.preferred_name.data:
            user.preferred_name = user.username
        else:
            user.preferred_name = form.preferred_name.data
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash(f'Added the user: {user.username}')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login&register.html', type="Register", form=form)


@app.route('/submissions')
@login_required
def submissions():
    submissions = []
    for i in range(0, 12):
        submissions.append({'date': str(date.today()), 'accuracy': round(random.randint(0, 10) / 10, 2), 
            'time_taken': round(random.uniform(0.0, 30.0), 2)})
    return render_template('submissions.html', submissions=submissions)


@app.route('/validate_registration', methods=['POST'])
def validate_registration():
    json = request.form
    if json and 'username' in json.keys():
        username = json['username']
        print(username)
        username_available = User.query.filter_by(username=username).first() == None
        print(f'username available?: {username_available}')
        return jsonify({'available': username_available})
    elif json and 'email' in json.keys():
        email = json['email']
        print(email)
        email_available = User.query.filter_by(email=email).first() == None
        print(f'email available?: {email_available}')
        return jsonify({'available': email_available})
    return redirect(url_for('login'))





