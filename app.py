from flask import Flask
from dbase import User, Comment, Suggestion, db

app = Flask(__name__)

db.create_all()

#user13 = User("tot", "tot@sisi.com")
#db.session.add(user13)
#db.session.commit()


#@app.route('/')
def get_user():
    return str(User.query.all())



@app.route('/')
def get_comment():
    return str(User.query.filter_by(id=1).first())


if __name__ == '__main__':
    app.run(debug=True)
