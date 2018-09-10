# NOTE stolen from tutorial https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_babel import _


class LoginForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_('Remember Me'))
    submit = SubmitField(_('Sign In'))


class EventParamsForm(FlaskForm):
    city = StringField(_('City'), validators=[DataRequired()])
    country = StringField(_('Country'), validators=[DataRequired()])
    date_from = DateField(_('Date from'), default=date.today())
    date_to = DateField(_('Date to'), default=date.today())
    is_pilot = BooleanField(_('I am a pilot and will fly there'))
    submit = SubmitField(_('Find events'))


class NewEventForm(FlaskForm):
    name = StringField(_('Event name'), validators=[DataRequired()])
    desc = TextAreaField(_('Description'))
    city = StringField(_('City'), validators=[DataRequired()])
    country = StringField(_('Country'), validators=[DataRequired()])
    location = StringField(_('Location'), validators=[DataRequired()])
    from_ts = StringField(_('Date from'), validators=[DataRequired()])
    to_ts = StringField(_('Date to'), validators=[DataRequired()])
    submit = SubmitField(_('Add event'))


class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(_(
        'Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))
