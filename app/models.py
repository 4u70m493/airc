from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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

