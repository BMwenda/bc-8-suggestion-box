from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from flask_wtf import Form
from wtforms.validators import Length, DataRequired, EqualTo, Email


class RegistrationForm(Form):
    username = StringField('Username', [Length(min=4, max=25), DataRequired("Enter username")])
    email = StringField('Email Address', [Email("Enter email"), Length(min=6, max=35)])
    password = PasswordField('New Password', [DataRequired("Enter password"),
                              EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class LoginForm(Form):
    username = StringField('Username', [Length(min=4, max=25), DataRequired("Enter username")])
    password = PasswordField('Enter Password', [DataRequired("Enter your password")])
    submit = SubmitField('Log In')


class SuggestionForm(Form):
    title = StringField('Title', [Length(min=3, max=50), DataRequired("Enter a title")])
    description = TextAreaField(
        'Description', [Length(min=6, max=140), DataRequired("Description required")])
    submit = SubmitField('Suggest')


class CommentForm(Form):
    comment = TextAreaField('Comment', [Length(min=4, max=200), DataRequired("Comment required")])
