from blog import db, admin, current_datetime
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, abort


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


# Grants access to Admin Panel only to Admin.
class AdminPanelAccess(ModelView):
    
    def is_accessible(self):
        try:
            if current_user.username == "Admin" and current_user._is_admin == True:
                return current_user.is_authenticated
            else:
                return abort(404)
            
        except AttributeError:
            return abort(404)


admin.add_view(AdminPanelAccess(User, db.session))
