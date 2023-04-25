from blog import app
from flask import render_template
from blog.forms import SignupForm, LoginForm


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/signup", methods=("GET", "POST"))
def signup():
    form = SignupForm()
    return render_template("signup.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    return render_template("login.html", form=form)
