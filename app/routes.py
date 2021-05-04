from flask import render_template, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
def index():
    user = {'username': 'Allenator', 'preferred_name': 'Allen'}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template(url_for('login_or_register'), type="login", form=form)