from blog import app, db
from flask import render_template, redirect, url_for, flash
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
                    password=generate_password_hash(form.password.data, "scrypt"))

        db.session.add(user)
        db.session.commit()

        flash("The account has been created. You can log in now.", "success")
        return redirect(url_for("login"))

    return render_template("auth/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        password = check_password_hash(user.password,
                                       form.password.data)

        if password:
            flash(f"Successfully logged in. Welcome {user.username} :)", "success")
            return redirect(url_for("user_dashboard"))

        return redirect(url_for("login"))

    return render_template("auth/login.html", form=form)


@app.route("/user_dashboard", methods=["GET", "POST"])
def user_dashboard():
    return render_template("user/dashboard.html")
