# NOTE stolen from tutorial https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EventParamsForm(FlaskForm):
    city = StringField('City')
    country = StringField('Country')
    date_from = DateField('Date from', default=date.today())
    date_to = DateField('Date to', default=date.today())
    is_pilot = BooleanField('I am a pilot and will fly there')
    submit = SubmitField('Find events')


class NewEventForm(FlaskForm):
    name = StringField('Event name')
    desc = TextAreaField('Description')
    city = StringField('City')
    country = StringField('Country')
    location = StringField('Location')
    from_ts = StringField('Date from')
    to_ts = StringField('Date to')
    submit = SubmitField('Add event')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
