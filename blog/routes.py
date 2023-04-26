from blog import app, bcrypt, db
from flask import render_template, redirect, url_for
from blog.forms import SignupForm, LoginForm
from blog.models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/signup", methods=("GET", "POST"))
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # Hash of the password given in the form
        hashed_password = bcrypt.generate_password_hash(form.password.data, 14).decode("utf-8")

        # User data from the form to the database
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)

        # Add and save user data to the database
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check if a user exists in the database
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            # Check that the user's password is the same as the one in the database
            user_password = bcrypt.check_password_hash(user.password, form.password.data)

            if user_password:
                return redirect(url_for("home"))
    else:
        return render_template("login.html", form=form)
