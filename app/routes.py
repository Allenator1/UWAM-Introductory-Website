import random
from datetime import date, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Quiz, Tutorial
from app.controller import *


@app.route('/', methods=['GET'])
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
    return redirect(url_for('register'))


@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    json = request.form
    tutorial = current_user.tutorial
    if json and 'fresh_tutorial' in json.keys():
        tutorial.new_tutorial()
        return redirect(url_for('tutorial'))
    elif json:
        question = list(json.keys())[0]
        tutorial.questions[question] = json[question]
        return jsonify({question: json[question]})
    return render_template('tutorial.html', tutorial=tutorial.questions)


@app.route('/feedback', methods=['GET'])
@login_required
def feedback():
    quiz = db.session.query(Quiz).join(User).filter_by(Quiz.user_id == current_user.id).\
        order_by(Quiz.finish_date).first()
    totals = get_section_totals(quiz)
    return render_template('feedback.html', totals=totals)


@app.route('/submissions')
@login_required
def submissions():
    submissions = db.query(Quiz).join(User).filter_by(Quiz.user_id == current_user.id).\
        order_by(Quiz.finish_date).limit(12).all()
    submissions_stats = []
    for quiz in submissions:
        stats = {}
        stats['quiz'] = quiz.finish_date
        totals = get_section_totals(quiz)
        stats['section'] = totals.index(max(totals)) + 1
        stats['accuracy'] = sum(totals) / 25
        stats['time_taken'] = (quiz.finish_time - quiz.start_time).total_seconds() / 60
        submissions_stats.append(stats)
    return render_template('submissions.html', submissions=submissions_stats)
    









