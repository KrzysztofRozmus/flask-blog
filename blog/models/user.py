from blog import db, current_datetime, admin
from flask import abort, redirect, url_for
from flask_login import current_user
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(163), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=current_datetime)
    profile_pic = db.Column(db.String(40), nullable=False, default="default_pic.png")
    _is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, email, password, date_joined, _is_admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.date_joined = date_joined
        self._is_admin = _is_admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_joined}', '{self._is_admin}')"


class UserView(ModelView):
    column_exclude_list = ["password", "profile_pic"]
    form_excluded_columns = ["date_joined", "profile_pic"]

    # The user will be granted access to the Admin Panel only if 3 conditions below are met.
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "Admin" and current_user._is_admin == True:
            return current_user.is_authenticated and current_user.username == "Admin" and current_user._is_admin == True
        else:
            return abort(403)


admin.add_view(UserView(User, db.session))
