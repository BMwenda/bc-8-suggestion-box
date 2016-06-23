from wtforms import StringField, PasswordField, validators, SubmitField
from flask_wtf import Form


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Enter Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    submit = SubmitField('Log In')


class SuggestionForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=50)])
    description = StringField(
        'Description', [validators.Length(min=6, max=140)])
    submit = SubmitField('Suggest')


class CommentForm(Form):
    comment = StringField('Comment', [validators.Length(min=4, max=140)])
