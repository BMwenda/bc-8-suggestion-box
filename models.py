""" Setting up the database """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    comment = db.relationship('Comment', backref='user',
                              lazy='dynamic')
    suggestion = db.relationship('Suggestion', backref='user',
                                 lazy='dynamic')

    def __init__(self, username, email, password, comment, suggestion):
        self.username = username
        self.email = email
        self.password = password
        self.comment = comment
        self.suggetion = suggestion

    def __repr__(self):
        return 'User {0}'.format(self.username)


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, description, posted_by):
        self.title = title
        self.description = description
        self.posted_by = posted_by


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    commented_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, comment, commented_by):
        self.comment = comment
        self.commented_by = commented_by