""" Setting up the database """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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
    pwd = db.Column(db.String(120), unique=True)
    comment = db.relationship('Comment', backref='user',
                              lazy='dynamic')
    suggestion = db.relationship('Suggestion', backref='user',
                                 lazy='dynamic')

    def __init__(self, username, email, pwd, comment, suggestion):
        self.username = username
        self.email = email
        self.pwd = pwd
        self.comment = comment
        self.suggetion = suggestion

    def __repr__(self):
        return 'User {0}'.format(self.username)


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    poster = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, description, poster):
        self.title = title
        self.description = description
        self.poster = poster


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    commenter = db.Column(db.Integer, db.ForeignKey('user.id'))


if __name__ == '__main__':
    manager.run()
