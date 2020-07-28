from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, URL

class RegisterForm(FlaskForm):
    """Form for registering users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])

class AnimeEditForm(FlaskForm):
    """Form for editing animes."""

    title = StringField('Title', validators=[DataRequired()])
    season = SelectField('Season', choices=[('spring', 'Spring'), ('summer', 'Summer'),
    ('fall', 'Fall'), ('winter', 'Winter')], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    airing_datetime = DateTimeField('Air Date and Time')
    image = StringField('Image URL', validators=[URL()])
    description = TextAreaField('Description')
    watch_link = StringField('Streaming Link')