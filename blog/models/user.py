from blog import db, current_datetime, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(163), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=current_datetime)
    profile_pic = db.Column(db.String(40), nullable=False, default="default_pic.png")

    def __init__(self, username, email, password, date_joined):
        self.username = username
        self.email = email
        self.password = password
        self.date_joined = date_joined

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_joined}')"


class UserView(ModelView):
    column_exclude_list = ["password", "profile_pic"]
    form_excluded_columns = ["date_joined", "profile_pic"]


admin.add_view(UserView(User, db.session))
