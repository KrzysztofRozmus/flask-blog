from blog import app, db
from flask import render_template, redirect, url_for
from blog.forms.auth import SignupForm, LoginForm
from blog.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():

    return render_template("base.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("auth/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one()
        password = check_password_hash(user.password,
                                       form.password.data)

        if password:
            return redirect(url_for("signup"))

        return redirect(url_for("login"))

    return render_template("auth/login.html", form=form)
