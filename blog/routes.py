from blog import app, bcrypt, db, login_manager
from flask import render_template, redirect, url_for, flash
from blog.forms import SignupForm, LoginForm
from blog.models import User
from datetime import timedelta
from flask_login import login_user, login_required, logout_user, current_user


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/signup", methods=("GET", "POST"))
def signup():
    form = SignupForm()

    if current_user.is_authenticated:
        return redirect(url_for("user_dashboard"))

    elif form.validate_on_submit():
        # Hash of the password given in the form
        hashed_password = bcrypt.generate_password_hash(form.password.data, 14).decode("utf-8")

        # User data from the form to the database
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)

        # Add and save user data to the database
        db.session.add(user)
        db.session.commit()

        flash("The account was successfully created. You can log in now.", "success")
        return redirect(url_for("login"))
    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("user_dashboard"))

    elif form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        login_user(user, remember=True, duration=timedelta(minutes=1))

        flash(f"Logged in successfully. Hello {current_user.username} :)", "success")
        return redirect(url_for("user_dashboard"))
    else:
        return render_template("login.html", form=form)


@app.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    return render_template("user_dashboard.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been log out", "info")
    return redirect(url_for("home"))
