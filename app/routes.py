from datetime import datetime
from flask import json, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Quiz
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
    elif json:
        question = list(json.keys())[0]
        tutorial.questions[question] = json[question]
        return
    return render_template('tutorial.html', questions=tutorial.questions)


@app.route('/feedback', methods=['GET'])
@login_required
def feedback():
    quiz = db.session.query(Quiz).join(User).\
        filter(Quiz.user_id == current_user.id, Quiz.finish_date != None).\
        order_by(Quiz.finish_date.desc()).first()
    section_totals = get_section_totals(quiz)
    section_proportions = get_proportions(section_totals)
    section = max(section_totals, key=section_totals.get)
    return render_template('feedback.html', section_proportions=section_proportions, section=section)


@app.route('/submissions', methods=['GET', 'POST'])
@login_required
def submissions():
    submissions = db.session.query(Quiz).join(User).\
        filter(Quiz.user_id == current_user.id, Quiz.finish_date != None).\
        order_by(Quiz.finish_date.desc()).limit(12).all()

    submission_stats = []
    aggr_section_totals = {'Finance': 0, 'Marketing': 0, 'Chassis': 0, 'Vehicle Dynamics': 0, 'Powertrain': 0}

    if submissions == []:
        return render_template('submissions.html', submission_stats=submission_stats, 
            section_proportions=aggr_section_totals, section="NIL")

    for quiz in submissions:
        stats = {}
        stats['date'] = quiz.finish_date
        stats['quiz_id'] = quiz.id
        section_totals = get_section_totals(quiz)
        aggr_section_totals = {k:(aggr_section_totals[k] + section_totals[k]) for k in section_totals.keys()}
        stats['section'] = max(section_totals, key=section_totals.get)
        stats['time_taken'] = round((quiz.finish_date - quiz.start_date).total_seconds() / 60, 2)
        submission_stats.append(stats)

    section = max(section_totals, key=aggr_section_totals.get)
    return render_template('submissions.html', submission_stats=submission_stats, section_proportions=get_proportions(aggr_section_totals),
        section=section)


@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id=None):
    quiz = None
    if quiz_id:
        quiz = Quiz.query.get(quiz_id)
    elif not current_user.current_quiz:
        quiz = Quiz(user_id=current_user.id)
        db.session.add(quiz)
        db.session.commit()
        current_user.current_quiz = quiz.id
    else:    
        quiz = Quiz.query.get(current_user.current_quiz)

    if request.method == 'POST' and not quiz_id:
        if is_completed(quiz):
            quiz.finish_date = datetime.utcnow()
            current_user.current_quiz = None
            db.session.commit()
            return redirect(url_for('feedback'))

    db.session.commit()
    return render_template('quiz.html.jinja', finance_qs=quiz.finance, marketing_qs=quiz.marketing,
        chassis_qs=quiz.chassis, vehicle_dynamics_qs=quiz.vehicle_dynamics, powertrain_qs=quiz.powertrain, 
        old_submission=bool(quiz_id))


@app.route('/new_quiz', methods=['GET'])
@login_required
def new_quiz():
    assert(current_user.current_quiz is not None)
    old_quiz = Quiz.query.get(current_user.current_quiz)
    db.session.delete(old_quiz)
    current_user.current_quiz = None
    db.session.commit()
    return redirect(url_for('quiz'))


@app.route('/del_quiz', methods=['GET', 'POST'])
@login_required
def del_quiz():
    if request.form and 'del_submission' in request.form.keys():
        submission_id = int(request.form['del_submission'])
        assert(Quiz.query.get(submission_id) is not None)
        db.session.delete(Quiz.query.get(submission_id))
        db.session.commit()
        return jsonify(status="success")


@app.route('/save_answer', methods=['POST'])
@login_required
def save_answer():
    quiz = Quiz.query.get(current_user.current_quiz)
    if request.method == 'POST' and request.form:
        response = request.form  
        key = list(response.keys())[0]
        department = key.split('-')[0]
        question = key.split('-')[1]

        if len(key.split('-')) > 2:
            response = request.form.getlist(key)
            answer = response[1]
            is_toggled = response[0] == "on"
            current_ans_list = getattr(quiz, department)[question]
            answer_exists = answer in current_ans_list

            if current_ans_list == "" and is_toggled:
                current_ans_list = [answer]
            elif not answer_exists and is_toggled:
                current_ans_list.append(answer)
            elif answer_exists and not is_toggled:
                current_ans_list.remove(answer)

            getattr(quiz, department)[question] = current_ans_list
        else:
            getattr(quiz, department)[question] = response[key]

        db.session.commit()
        return jsonify(successful=True)
    return redirect(url_for('quiz'))



        



    









