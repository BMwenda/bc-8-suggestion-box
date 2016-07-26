from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Migrate db to flask
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def set_password(self, pswd):
        self.password = generate_password_hash(pswd)

    def check_password(self, pswd):
        return check_password_hash(self.password, pswd)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Suggestion(db.Model):

    __tablename__ = 'suggestions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(
        'User', backref=db.backref('suggestions', lazy='dynamic'))
    votes = db.Column(db.Integer)
    flags = db.Column(db.Integer)

    def __init__(self, title, description, user_id, votes=0, flags=0):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.votes = votes
        self.flags = flags

    def __repr__(self):
        return '<Suggestion %r>' % (self.title)


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Establish a relationship with 'users' table
    user = db.relationship(
        'User', backref=db.backref('comments', lazy='dynamic'))
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))
    # Relationship with 'suggestions' table
    suggestion = db.relationship(
        'Suggestion', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, comment, user_id):
        self.comment = comment
        self.user_id = user_id
        # self.suggestion_id = suggestion_id

    def __repr__(self):
        return '<Comment %r>' % (self.comment)

if __name__ == '__main__':
    manager.run()
