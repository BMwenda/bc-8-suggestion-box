from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, LoginManager
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def encrypt_password(self, password):
        self.password_hash = generate_password_hash(password)

    def decrypt_password(self, password_hash):
        return check_password_hash(self.password_hash, password_hash)

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return (self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(140))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    suggestion = db.relationship('User', backref=db.backref('user',
                                                            lazy='dynamic'))
    votes = db.Column(db.Integer)
    flags = db.Column(db.Integer)

    def __init__(self, title, description, posted_by=None, votes=None, flags=None):
        self.title = title
        self.description = description
        self.posted_by = posted_by
        self.votes = votes
        self.flags = flags


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    commented_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    comm = db.relationship('User', backref=db.backref('comment',
                                                      lazy='dynamic'))

    def __init__(self, comment):
        self.comment = comment
        # self.commented_by = commented_by

if __name__ == '__main__':
    manager.run()
