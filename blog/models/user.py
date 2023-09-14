from flask import abort, flash, redirect, url_for
from blog import db, admin, current_datetime
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import UserMixin
from flask_admin.menu import MenuLink


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


# Method adds Blog link in Admin Panel for home page of the blog
admin.add_link(MenuLink(name='Blog', url='/'))

# Method adds Logout link in Admin Panel for logout view
admin.add_link(MenuLink(name='Logout', url='/logout'))


class UserView(ModelView):
    # Enabling CSRF Protection
    form_base_class = SecureForm

    column_exclude_list = ["password", "profile_pic"]
    form_excluded_columns = ["date_joined", "profile_pic"]

    def is_accessible(self):
        """The user will be granted access to the Admin Panel only if 3 conditions below are met"""
        if current_user.is_authenticated and current_user.username == "Admin" and current_user._is_admin == True:
            return current_user.is_authenticated and current_user.username == "Admin" and current_user._is_admin == True
        else:
            return abort(403)

    def on_model_delete(self, model):
        """This method does not allow to delete the Admin account"""
        if model.username == "Admin":
            flash("Admin account cannot be deleted", "danger")

            # user.details_view is one of the many endpoints that can be redirect to.
            # "user" object came from models and it's added to Admin Panel.
            abort(redirect(url_for("user.details_view")))

    def on_model_change(self, form, model, is_created):
        """This method does not allow to change the Admin username.
        Is in addition to the edit_form method"""

        # Check that the user is edited, not created.
        if not is_created:

            # If "Admin" user is edited, block the change.
            if "Admin" in form.username.data and model.username != "Admin":
                flash("Admin username cannot be changed", "danger")
                abort(redirect(url_for("user.edit_view")))

        return super().on_model_change(form, model, is_created)

    def edit_form(self, obj):
        """This method disables editing of the Admin username field.
        Is in addition to the on_model_change method."""

        # Download the editing form.
        form = super(UserView, self).edit_form(obj)

        # Block editing of the username column.
        if form.username.data == "Admin":
            form.username.render_kw = {'readonly': True}

        return form

admin.add_view(UserView(User, db.session))
