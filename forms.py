# NOTE stolen from tutorial https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_babel import lazy_gettext as _l

from app.models import User

default_from_date = datetime.date.today()
default_to_date = default_from_date + datetime.timedelta(days=45)

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class EventParamsForm(FlaskForm):
    city = StringField(_('City'), validators=[DataRequired()])
    country = StringField(_('Country'), validators=[DataRequired()])
    date_from = DateField(_('Date from', format='%Y-%m-%d'), default=default_from_date)
    date_to = DateField(_('Date to', format='%Y-%m-%d'), default=default_to_date)
    is_pilot = BooleanField(_('I am a pilot and will fly there'))
    submit = SubmitField(_('Find events'))


class NewEventForm(FlaskForm):
    name = StringField(_l('Event name'), validators=[DataRequired()])
    desc = TextAreaField(_l('Description'))
    city = StringField(_l('City'), validators=[DataRequired()])
    country = StringField(_l('Country'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    from_ts = DateField(_l('Date from', format='%Y-%m-%d'), default=default_from_date, validators=[DataRequired()])
    to_ts = DateField(_l('Date to', format='%Y-%m-%d'), default=default_to_date, validators=[DataRequired()])
    submit = SubmitField(_l('Add event'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l(
        'Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))
