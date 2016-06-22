from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])


class SuggestionForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=50)])
    description = StringField(
        'Description', [validators.Length(min=6, max=140)])


class CommentForm(Form):
    comment = StringField('Comment', [validators.Length(min=4, max=140)])
