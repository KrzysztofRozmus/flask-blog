from blog import db, current_datetime, admin
from flask import abort, flash, redirect, url_for
from flask_login import current_user
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(163), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=current_datetime)
    profile_pic = db.Column(db.String(40), nullable=False, default="default_pic.png")
    _is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, date_joined, _is_admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.date_joined = date_joined
        self._is_admin = _is_admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_joined}', '{self._is_admin}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=current_datetime)
    author = db.Column(db.String, nullable=False, default="Admin")

    def __init__(self, title, content, author, date_posted=None):
        self.title = title
        self.content = content
        self.author = author
        self.date_posted = date_posted

    def __repr__(self):
        return f"User('{self.title}', '{self.content}', '{self.author}', '{self.date_posted}')"


class UserView(ModelView):
    # Enabling CSRF Protection
    form_base_class = SecureForm
    column_exclude_list = ["password", "profile_pic"]
    form_excluded_columns = ["date_joined", "profile_pic"]

    # The user will be granted access to the Admin Panel only if 3 conditions below are met.
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "Admin" and current_user._is_admin == True:
            return current_user.is_authenticated and current_user.username == "Admin" and current_user._is_admin == True
        else:
            return abort(403)

    # This function does not allow to delete the Admin account.
    def on_model_delete(self, model):
        if model.username == "Admin":
            flash("Admin account cannot be deleted", "danger")

            # user.details_view is one of the many endpoints that can be redirect to.
            # "user" object came from models and it's added to Admin Panel.
            abort(redirect(url_for("user.details_view")))


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class PostView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {"content": CKTextAreaField}
    form_excluded_columns = ["author", "date_posted"]


admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
