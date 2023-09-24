from blog import app, db, login_manager, current_datetime, mail, serializer
from flask_login import (login_user, login_required, logout_user,
                         fresh_login_required, login_fresh, current_user)
from flask import render_template, redirect, url_for, flash
from blog.forms.auth import SignupForm, LoginForm
from blog.forms.comment import CommentForm
from blog.forms.user import UserForm, ProfilePicForm, ChangePasswordButton, ChangePasswordForm
from blog.models.user import User
from blog.models.post import Post
from blog.models.comment import Comment
from datetime import timedelta
from blog.functions import save_profile_picture, delete_profile_picture
from flask_mail import Message
import os


# ============================= load_user ==============================
@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))


# ============================= home ==============================
@app.route("/")
def home():
    # Variable for displaying posts only on home page.
    home_page = True

    posts = db.session.execute(db.select(Post).order_by(Post.date_posted)).scalars()
    return render_template("base.html", posts=posts, home_page=home_page)


# ============================= signup ==============================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if current_user.is_authenticated and current_user.is_active:
        flash("You are signed up and logged in already", "info")
        return redirect(url_for("user_dashboard"))

    if form.validate_on_submit():
        if form.username.data == "Admin":
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        date_joined=current_datetime,
                        _is_admin=True)
        else:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        date_joined=current_datetime)

        db.session.add(user)
        db.session.commit()

        flash("The account has been created. You can log in now.", "success")
        return redirect(url_for("login"))

    return render_template("auth/signup.html", form=form)


# ============================= login ==============================
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if login_fresh():
        flash("You are logged in already", "info")
        return redirect(url_for("user_dashboard"))

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()

        login_user(user, remember=True, duration=timedelta(minutes=1))

        if current_user.username == "Admin" and current_user._is_admin == True:
            return redirect(url_for("admin.index"))

        flash(f"Successfully logged in. Welcome {user.username} :)", "success")
        return redirect(url_for("user_dashboard"))

    return render_template("auth/login.html", form=form)


# ============================= logout ==============================
@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash("You have been log out.", "info")
    return redirect(url_for("login"))


# ============================= user_dashboard ==============================
@app.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    number_of_user_comments = db.session.query(Comment).filter_by(user_id=current_user.id).count()

    pic_file = url_for("static", filename=f"profile_pics/{current_user.profile_pic}")
    return render_template("user/dashboard.html", pic_file=pic_file, number_of_user_comments=number_of_user_comments)


# ============================= settings ==============================
@app.route("/settings/<int:id>", methods=["GET", "POST"])
@fresh_login_required
def settings(id):
    form = UserForm()
    profile_pic_form = ProfilePicForm()
    button_form = ChangePasswordButton()

    pic_file = url_for("static", filename=f"profile_pics/{current_user.profile_pic}")

    user = db.session.execute(db.select(User).filter_by(id=id)).scalar()

    # This if statement is used because of two forms on the same page.
    # Validate_on_submit()function triggers both submit buttons at the same time.
    if form.submit.data and form.validate():
        if form.username.data == "":
            pass
        else:
            user.username = form.username.data

        if form.email.data == "":
            pass
        else:
            user.email = form.email.data

        db.session.commit()

        flash("Data changed successfully", "success")
        return redirect(url_for("user_dashboard"))

    elif profile_pic_form.submit_pic.data and profile_pic_form.validate():
        if profile_pic_form.picture.data == None:
            pass
        else:
            profile_picture = save_profile_picture(profile_pic_form)

            # Remove previous unused profile pic, from profile pics directory to save space.
            if current_user.profile_pic == "default_pic.png":
                pass
            else:
                try:
                    delete_profile_picture(app.config['UPLOAD_FOLDER'])
                except FileNotFoundError:
                    pass

            user.profile_pic = profile_picture
            db.session.commit()

            flash("Profile picture changed successfully", "success")
            return redirect(url_for("settings", id=id))

    elif button_form.submit_button.data and button_form.validate():
        msg = Message(subject="Change your password",
                      recipients=[current_user.email],
                      sender=app.config["MAIL_USERNAME"])

        token = serializer.dumps(user.email)

        link = url_for("change_user_password", token=token, _external=True)

        msg.body = f"Click to change password: {link}"

        try:
            mail.send(msg)
            flash(f"Email was sent successfully. Check mailbox", "success")
            return redirect(url_for("settings", id=id))

        except Exception:
            flash("Email was not sent, try again.", "danger")
            return redirect(url_for("settings", id=id))

    return render_template("user/settings.html",
                           form=form,
                           profile_pic_form=profile_pic_form,
                           user_data_to_update=user,
                           pic_file=pic_file,
                           button_form=button_form)


# ============================= post_page ==============================
@app.route("/posts_page/<int:id>", methods=["GET", "POST"])
def posts_page(id):
    add_new_comment_form = CommentForm()
    post = db.get_or_404(Post, id)
    number_of_comments = db.session.query(Comment).count()

    # Inner join is used here.
    '''
    SELECT user.username, comment.date_posted, comment.content,  
    FROM comment
    JOIN user ON comment.user_id = user.id
    '''
    comments = db.session.query(User.username, Comment.date_posted, Comment.content).join(User).all()

    if add_new_comment_form.validate_on_submit():
        new_comment = Comment(content=add_new_comment_form.content.data,
                              user_id=current_user.id,
                              post_id=id)

        db.session.add(new_comment)
        db.session.commit()

        flash("Comment added successfully", "success")
        return redirect(url_for("posts_page", id=post.id))

    return render_template("posts_page.html",
                           post=post,
                           add_new_comment_form=add_new_comment_form,
                           comments=comments,
                           number_of_comments=number_of_comments)


# ============================= delete_account ==============================
@app.route("/delete_account/<int:id>", methods=["GET"])
def delete_account(id):
    try:
        if current_user.id == id:
            user_to_delete = db.get_or_404(User, id)
            db.session.delete(user_to_delete)

            db.session.commit()

            # Delete user profile pic after deleting an account to save space.
            try:
                profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.profile_pic)
                os.remove(profile_pic_path)
            except FileNotFoundError:
                pass

            # logout_user prevents flash messages from being displayed when redirected to the login page.
            logout_user()

            flash("The account has been deleted", "success")
            return redirect(url_for("login"))

    except AttributeError:
        flash("You don't have permission to this action", "danger")
        return redirect(url_for("home"))


# ============================= change_user_password ==============================
@app.route("/change_user_password/<token>", methods=["GET", "POST"])
def change_user_password(token):
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user_email = serializer.loads(token, max_age=80)
        user = db.session.execute(db.select(User).filter_by(email=user_email)).scalar()

        user.password = form.new_password.data
        db.session.commit()

        flash("Password has been successfully changed", "success")
        return redirect(url_for("login"))

    return render_template("user/change_user_password.html", form=form)
