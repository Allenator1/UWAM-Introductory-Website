from flask import render_template, redirect, url_for
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def index():
    user = {'username': 'Allen', 'preferred_name': 'A'}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login_or_register.html', type="Login", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login_or_register.html', type="Register", form=form)

