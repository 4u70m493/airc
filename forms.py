# NOTE stolen from tutorial https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EventParamsForm(FlaskForm):
    city = StringField('City')
    country = StringField('Country')
    date_from = StringField('Date from')
    date_to = StringField('Date to')
    is_pilot = BooleanField('I am a pilot and will fly there')
    submit = SubmitField('Find events')
