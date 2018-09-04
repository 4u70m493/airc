from flask import Flask
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from forms import LoginForm, EventParamsForm

# Libs for functionality
import calendar as cal

# Own modules from root dir
from config import Config

app = Flask(__name__)
app.config.from_object(Config) # TODO rewrite to reading a dedicated file

@app.route('/')
def show_form():
    form = EventParamsForm()
    return render_template('index.html', title='Find best airshows around', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign in', form=form)


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


if __name__ == '__main__':
    app.run(debug=True)
