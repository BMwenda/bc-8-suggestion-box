from flask import Flask, request, render_template, redirect
from models import db, User, Suggestion, Comment
from forms import RegistrationForm, SuggestionForm, CommentForm

app = Flask(__name__)

db.create_all()


# def add_user():
#    user13 = User("tot", "tot@sisi.com")
#   db.session.add(user13)
#    db.session.commit()

#@app.route('/', methods=['GET', 'POST'])
def get_user():
    return str(User.query.all())


def add_suggestion():
    sugg = Suggestion("Good idea!", "I like your approach", "user.id")
    db.session.add(sugg)
    db.session.commit()


#@app.route('/', methods=['GET', 'POST'])
def get_suggestion():
    return str(Suggestion.query.all())


#@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return ('Thanks for registering')
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def suggest():
    form = SuggestionForm(request.form)
    if request.method == 'POST' and form.validate():
        suggestion = Suggestion(form.title.data, form.description.data)
        db.session.add(suggestion)
        db.session.commit()
        return ('Thanks for your suggestion!')
        return redirect('/')
    return render_template('suggest.html', form=form)


#@app.route('/', methods=['GET', 'POST'])
def comment():
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = Comment(form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return ('Thanks for commenting!')
        return redirect('/')
    return render_template('suggest.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def get_members():
    return str(User.query.all())

if __name__ == '__main__':
    app.run(debug=True)
