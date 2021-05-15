from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Quiz
from app.controller import *
from operator import add


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
    return render_template('tutorial.html', questions=tutorial.questions)


@app.route('/feedback', methods=['GET'])
@login_required
def feedback():
    quiz = db.session.query(Quiz).join(User).\
        filter(Quiz.user_id == current_user.id).\
        order_by(Quiz.finish_date).first()
    section_totals = get_section_totals(quiz)
    section_proportions = get_proportions(section_totals)
    section = section_totals.index(max(section_totals)) + 1
    return render_template('feedback.html', section_proportions=section_proportions, section=section)


@app.route('/submissions')
@login_required
def submissions():
    submissions = db.session.query(Quiz).join(User).\
        filter(Quiz.user_id == current_user.id, Quiz.finish_date != None).\
        order_by(Quiz.finish_date).limit(12).all()
    submission_stats = []
    aggregate_section_totals = [0, 0, 0, 0, 0]
    for quiz in submissions:
        stats = {}
        stats['date'] = quiz.finish_date
        section_totals = get_section_totals(quiz)
        aggregate_section_totals = list(map(add, aggregate_section_totals, section_totals))
        stats['section'] = section_totals.index(max(section_totals)) + 1
        stats['time_taken'] = round((quiz.finish_date - quiz.start_date).total_seconds() / 60, 2)
        submission_stats.append(stats)
    section = aggregate_section_totals.index(max(aggregate_section_totals)) + 1
    return render_template('submissions.html', submission_stats=submission_stats, section_proportions=get_proportions(aggregate_section_totals),
        section=section)


@app.route('/old_quiz')
@login_required
def old_quiz():
    pass

    









