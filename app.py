from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, User, Suggestion, Comment
from forms import RegistrationForm, SuggestionForm, CommentForm, LoginForm
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
# Load csrprotect
CsrfProtect(app)
# Create a secret key to prevent a CSRF attack
app.secret_key = "siri-kubwa"
WTF_CSRF_SECRET_KEY = 'wtf i hate you'

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """This function logins in a user and creates a session"""
    form = LoginForm()
    if form.validate_on_submit():
        # If validation is successful, create an instance of the user
        user = User.query.filter_by(username=form.username.data).first()
        # Login user
        login_user(user)
        flash('You are now logged in')
        next = request.args.get('next')
        # next checks if user valid creds to
        # access the next url
        if not next:
            flash("You don't have permission to access this page")
            return redirect(url_for('home'))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base.html'))

@app.route('/')
def home():
    return render_template('base.html')


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/suggest', methods=['GET', 'POST'])
@login_required
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
@login_required
def add_comment():
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = Comment(comment=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('add_comment'))
    return render_template('comment.html', form=form)


@app.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    # query to view all suggestions by all users
    return render_template('view_all_suggestions.html')


@app.route('/user_suggestions', methods=['GET', 'POST'])
@login_required
def user_suggestions():
    # query to view all suggestions made by the user
    return render_template('user_suggestions.html')


@app.route('/comments', methods=['GET', 'POST'])
@login_required
def comments():
    # Query to view all comments by all users
    return render_template('view_all_comments.html', Comment=comments)


@app.route('/user_comments', methods=['GET', 'POST'])
@login_required
def user_comments():
    # query to view all comments by the user
    return render_template('user_comments.html')

@login_required
def delete_suggestion():
    # method to delete user suggestion
    return render_template('user_suggestions.html')

@login_required
def up_vote_suggestion():
    # add method to implement up voting
    return redirect(url_for('view_all_suggestions.html'))

@login_required
def down_vote_suggestion():
    # method to implement down voting
    return render_template('view_all_suggestions.html')

@login_required
def flag():
    # add a method to implement flagging comments
    return render_template('view_all_comments.html')

if __name__ == '__main__':
    app.run(debug=True)
