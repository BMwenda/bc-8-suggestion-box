from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, User, Suggestion, Comment
from forms import RegistrationForm, SuggestionForm, CommentForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

app = Flask(__name__)
# Create a secret key to prevent a CSRF attack
app.secret_key = "some_hash_key"
# Create a login_manager class that lets the app
# and Flask-Login work together
login_manager = LoginManager()
# Configuring the login object for login
login_manager.init_app(app)

# Creating a user_loader call back.
# Will reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:  # and user.decrypt_password(form.password):
            login_user(user)
            return redirect(url_for('add_suggestion'))
        else:
            flash("Invalid credentials! Not a user? Sign up first")
            # return redirect(url_for('register'))
    return render_template('login.html', form=form)


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/suggest', methods=['GET', 'POST'])
def add_suggestion():
    form = SuggestionForm(request.form)
    if request.method == 'POST' and form.validate():
        suggestion = Suggestion(title=form.title.data,
                                description=form.description.data)
        db.session.add(suggestion)
        db.session.commit()
        return redirect(url_for('add_suggestion'))
    return render_template('suggest.html', form=form)


@app.route('/comment', methods=['GET', 'POST'])
def add_comment():
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = Comment(comment=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('add_comment'))
    return render_template('comment.html', form=form)


@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    # return str(Suggestion.query.all())
    # return redirect(url_for('index.html'))
    return render_template('view_all_suggestions.html')


@app.route('/user_suggestions', methods=['GET', 'POST'])
def user_suggestions():
    # return str(Suggestion.query.all())
    # return redirect(url_for('index.html'))
    return render_template('user_suggestions.html')


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    comments = User.query.all()
    # return redirect(url_for('index.html'))
    return render_template('view_all_comments.html', Comment=comments)


@app.route('/user_comments', methods=['GET', 'POST'])
def user_comments():
    # return str(Suggestion.query.all())
    # return redirect(url_for('index.html'))
    return render_template('view_user_comments.html')


def delete_suggestion():
    suggestion = Suggestion.query.get(id)
    db.session.delete(suggestion)
    db.session.commit()
    flash("Suggestion deleted successfully")
    return redirect(url_for("suggest"))


def up_vote_suggestion():
    v = Suggestion.query.first()
    v.votes = Suggestion.votes + 1
    flash("Record deleted!")
    return redirect(url_for("suggest"))


def down_vote_suggestion():
    v = Suggestion.query.first()
    if v.votes < 1:
        pass
    v.votes = Suggestion.votes - 1
    flash("Record deleted!")
    return redirect(url_for("suggest"))

if __name__ == '__main__':
    app.run(debug=True)
