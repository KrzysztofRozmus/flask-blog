from blog import app
from flask import render_template
from blog.forms.auth import SignupForm, LoginForm


@app.route("/")
def home():

    return render_template("base.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    return render_template("auth/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    return render_template("auth/login.html", form=form)
