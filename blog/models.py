from blog import db, admin, current_datetime
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=current_datetime)
    _is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, _is_admin=None):
        self.username = username
        self.email = email
        self.password = password
        self._is_admin = _is_admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.Date, nullable=False, default=current_datetime.date())
    time_posted = db.Column(db.Time, nullable=False, default=current_datetime.time())
    author = db.Column(db.String, nullable=False, default="Admin")

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return f"User('{self.title}', '{self.content}', '{self.author}')"


# Grants access to Admin Panel only to Admin.
class UserView(ModelView):
    column_exclude_list = ["password"]

    def is_accessible(self):
        try:
            if current_user.username == "Admin" and current_user._is_admin == True:
                return current_user.is_authenticated
            else:
                return abort(404)

        except AttributeError:
            return abort(404)


class PostView(ModelView):
    column_exclude_list = ["content"]
    form_excluded_columns = ["author", "date_posted", "time_posted"]


admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))