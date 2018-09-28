from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from flask_babel import gettext as _, lazy_gettext as _l

# local stuff
from .models import User, Event, Location
from .helpers import form2datetime
from forms import LoginForm, EventParamsForm, RegistrationForm, NewEventForm, NewLocationForm

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
        #flash("Got: city, country, dates! Nice!")  # TODO implement actual search + return results!
        e = Event()
        events = Event.get_on_criteria(e, from_ts=date_from, to_ts=date_to, city=city, country=country).all()
        return render_template('search-results.html', events=events)
    return render_template('index.html', title=_('Find best airshows around'), form=form)

@app.route('/map')
def map():
    mapbox_key = app.config.get('MAPBOX_KEY')
    if not mapbox_key:
        flash("Could not retrieve mapbox key! Will not draw the map! Check .env")
    return render_template('map.html', title=_('Map!'), key=mapbox_key)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('my-events'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        #flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title=_('Register'), form=form)


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
    return render_template('login.html', title=_('Sign in'), form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/event/<event_id>')
def show_event(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    return render_template('event.html', event=event)


@app.route('/plan/<event_id>')
@login_required
def plan(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash('Event {} not found.'.format(event_id))
        return redirect(url_for('my-events'))
    current_user.plan(event)
    db.session.commit()
    flash("You've planned {}!".format(event.name))
    return redirect(url_for('my_events'))


@app.route('/unplan/<event_id>')
@login_required
def unplan(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        flash('Event {} not found.'.format(event_id))
        return redirect(url_for('my_events'))

    current_user.unplan(event)
    db.session.commit()
    flash('You have unplanned {}.'.format(event.name))
    return redirect(url_for('my_events'))


@login_required
@app.route('/my-events')
def my_events():
    events = current_user.get_planned_events().all()
    return render_template('my-events.html', events=events)


@login_required
@app.route('/new-event', methods=['GET', 'POST'])
def new_event():
    form = NewEventForm()
    if form.validate_on_submit():
        event = Event()
        event.name = form.name.data
        event.from_ts = form.from_ts.data
        event.to_ts = form.to_ts.data
        event.added_ts = datetime.utcnow()
        event.city = form.city.data
        event.country = form.country.data
        event.location_name = form.location.data
        event.desc = form.desc.data
        db.session.add(event)
        db.session.commit()

        flash('Congratulations, you have added new event: {}'.format(event.name))
        return redirect(url_for('show_event', event_id=event.id))
    return render_template('new-event.html', title='Add new event', form=form)

@login_required
@app.route('/new-location', methods=['GET', 'POST'])
def new_location():
    form = NewLocationForm()
    if form.validate_on_submit():
        l = Location()
        l.name = form.name.data
        l.city = form.city.data
        l.country = form.country.data
        l.desc = form.desc.data
        l.lat = form.lat.data
        l.lon = form.lon.data
        db.session.add(l)
        db.session.commit()

        flash(_l('Your location {} was added to the database, thanks!'.format(l.name)))
        return redirect(url_for('show_location', location_id=l.id))
    return render_template('new-location.html', title=_l('Add new location'), form=form)


@app.route('/calendar')
def show_calendar():
    c = cal.HTMLCalendar(cal.MONDAY)
    return c.formatmonth(2018,9)
