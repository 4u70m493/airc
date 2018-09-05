from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Event

# for forms
from flask_wtf import FlaskForm
from forms import LoginForm, EventParamsForm, RegistrationForm

# Libs for functionality
import calendar as cal


# Define supported routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EventParamsForm()
    if form.validate_on_submit():
        city = form.city.data
        country = form.country.data
        date_from = form.date_from.data
        date_to = form.date_to.data

        flash("Got: city, country, dates! Nice!")
    return render_template('index.html', title='Find best airshows around', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('my-events'))  # TODO fix, if any
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my-events')) # TODO fix, if any
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/event/<id>')
def show_event(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    return render_template('event.html', event=event)


@app.route('/plan/<id>')
@login_required
def plan(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash('Event {} not found.'.format(event_id))
        return redirect(url_for('my-events'))
    current_user.plan(event_id)
    db.session.commit()
    flash("You've planned {}!".format(event.name))
    return redirect(url_for('my-events'))


@app.route('/unplan/<id>')
@login_required
def unplan(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash('Event {} not found.'.format(event_id))
        return redirect(url_for('my-events'))

    current_user.unplan(event_id)
    db.session.commit()
    flash('You have unplanned {}.'.format(event.name))
    return redirect(url_for('my-events'))


@login_required
@app.route('/my-events')
def my_events():
    events = current_user.planned_events().all()
    return render_template('my-events.html', events=events)


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