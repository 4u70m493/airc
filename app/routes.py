from app import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User

# for forms
from flask_wtf import FlaskForm
from forms import LoginForm, EventParamsForm

# Libs for functionality
import calendar as cal


# Define supported routes
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EventParamsForm()
    return render_template('index.html', title='Find best airshows around', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/calendar')
def show_calendar():
    c = cal.HTMLCalendar(cal.MONDAY)
    return c.formatmonth(2018,9)


@app.route('/hello')
def hello_world():
    user = {'username': 'Test Testovich'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'I love vodka and 9!'
        },
        {
            'author': {'username': 'Vasya'},
            'body': 'I luv Guinness and cider!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)