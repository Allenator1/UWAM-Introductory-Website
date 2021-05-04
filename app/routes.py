from flask import render_template, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
def index():
    user = {'username': None, 'preferred_name': None}
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login_or_register.html', type="login", form=form)