from blog import app, db, login_manager, current_datetime
from flask import render_template, redirect, url_for, flash
from blog.forms.auth import SignupForm, LoginForm
from blog.forms.user import UserForm, LogoForm
from blog.models.user import User
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta
from werkzeug.utils import secure_filename
import os


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/")
def home():

    return render_template("base.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if current_user.is_authenticated and current_user.is_active:
        flash("You are signed up and logged in already", "info")
        return redirect(url_for("user_dashboard"))

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data, "scrypt"),
                    date_joined=current_datetime)

        db.session.add(user)
        db.session.commit()

        flash("The account has been created. You can log in now.", "success")
        return redirect(url_for("login"))

    return render_template("auth/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated and current_user.is_active:
        flash("You are logged in already", "info")
        return redirect(url_for("user_dashboard"))

    elif form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()

        login_user(user, remember=True, duration=timedelta(minutes=1))

        flash(f"Successfully logged in. Welcome {user.username} :)", "success")
        return redirect(url_for("user_dashboard"))

    return render_template("auth/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash("You have been log out.", "info")
    return redirect(url_for("login"))


@app.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():

    return render_template("user/dashboard.html")


@app.route("/settings/<int:id>", methods=["GET", "POST"])
@login_required
def settings(id):
    form = UserForm()
    logo_form = LogoForm()

    data_to_update = db.session.execute(db.select(User).filter_by(id=id)).scalar()

    if form.submit.data and form.validate():

        if form.username.data == "":
            pass
        else:
            data_to_update.username = form.username.data

        if form.email.data == "":
            pass
        else:
            data_to_update.email = form.email.data

        db.session.commit()
        flash("Data changed successfully", "success")
        return redirect(url_for("user_dashboard"))

    elif logo_form.submit_logo.data and logo_form.validate():
        if logo_form.photo.data == None:
            pass
        else:
            f = logo_form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.instance_path, 'photos', filename))

            flash("Logo changed successfully", "success")
            return redirect(url_for("user_dashboard"))

    return render_template("user/settings.html", form=form, logo_form=logo_form, data_to_update=data_to_update)
