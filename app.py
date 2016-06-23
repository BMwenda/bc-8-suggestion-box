from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, User, Suggestion, Comment
from forms import RegistrationForm, SuggestionForm, CommentForm, LoginForm
from flask_login import login_user, login_required, logout_user, LoginManager

app = Flask(__name__)
app.secret_key = "super secret key"
login_manager = LoginManager()
login_manager.init_app(app)

db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data)
        if user is not None and user.decrypt_password(form.password):
            login_user(user)
            flash('Welcome!')
            next = request.args.get('next')
            return redirect(next or url_for(add_suggestion))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        # session['user_id'] = user,id
        flash('Thanks for registering')
        return redirect(url_for(login))
    return render_template('register.html', form=form)


@app.route('/suggest', methods=['GET', 'POST'])
def add_suggestion():
    form = SuggestionForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        suggestion = Suggestion(title=form.title.data,
                                description=form.description.data)
        db.session.add(suggestion)
        db.session.commit()
        flash('Thanks for your suggestion!')
        return redirect(url_for(add_suggestion))
    return render_template('suggest.html', form=form)


@app.route('/all_suggestions', methods=['GET', 'POST'])
def view_all_suggestions():
    return str(Suggestion.query.all())
    return redirect(url_for('index.html'))


@app.route('/user_suggestions', methods=['GET', 'POST'])
def view_user_suggestions():
    return str(Suggestion.query.all())
    return redirect(url_for('index.html'))


@app.route('/all_comments', methods=['GET', 'POST'])
def view_all_comments():
    return str(Comment.query.all())
    return redirect(url_for('index.html'))


@app.route('/user_comments', methods=['GET', 'POST'])
def view_user_comments():
    return str(Suggestion.query.all())
    return redirect(url_for('index.html'))


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


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = Comment(form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash('Thanks for commenting')
        return redirect(url_for('comment'))
    return render_template('comment.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
