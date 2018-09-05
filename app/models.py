from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


plans = db.Table('plans',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    planned = db.relationship(
        'Event',
        secondary=plans,
        primaryjoin=(plans.c.user_id == id),
        secondaryjoin=(plans.c.event_id == id),
        backref=db.backref('plans', lazy='dynamic'), lazy='dynamic')  # TODO: recheck, is this right syntax or not.

    def plan(self, event):
        if not self.is_planning(event):
            self.planned.append(event)

    def unplan(self, event):
        if self.is_planning(event):
            self.planned.remove(event)

    def is_planning(self, event):
        return self.planned.filter(
            plans.c.user_id == event.id).count() > 0  # TODO: recheck this query expression!

    def planned_events(self):
        return Event.query.join(
            plans, (plans.c.event_id == Event.id)).filter(
            plans.c.user_id == self.id).order_by(
            Event.from_ts.asc())

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    from_ts = db.Column(db.DateTime)
    to_ts = db.Column(db.DateTime)
    added_ts = db.Column(db.DateTime, default=datetime.utcnow)
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    location = db.Column(db.String(255))

    def __repr__(self):
        return '<Event {}'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
