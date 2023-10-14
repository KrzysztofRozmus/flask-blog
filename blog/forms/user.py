from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, EmailField, SubmitField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length, ValidationError, DataRequired, EqualTo, Email
from blog.models.user import User
from blog import db


# ============================= UserForm ==============================
class UserForm(FlaskForm):
    username = StringField(validators=[Length(max=50)])
    email = EmailField(validators=[Length(max=50)])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user_username_in_db = db.session.execute(db.select(User).filter_by(username=username.data)).scalar()
            if user_username_in_db or current_user.username == "admin":
                raise ValidationError("That username is already taken.", "danger")
        else:
            raise ValidationError("This is your current username.", "danger")

    def validate_email(self, email):
        if email.data != current_user.email:
            user_email_in_db = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
            if user_email_in_db:
                raise ValidationError("That email is already taken.", "danger")
        else:
            raise ValidationError("This is your current email.", "danger")


# ============================= ProfilePicForm ==============================
class ProfilePicForm(FlaskForm):
    picture = FileField(validators=[FileAllowed(["jpg", "png", "gif"])])
    submit_pic = SubmitField("Update")


# ============================= ChangePasswordButton ==============================
class ChangePasswordButton(FlaskForm):
    submit_button = SubmitField("Send Link")


# ============================= ChangePasswordForm ==============================
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=3,)],
                                 render_kw={"placeholder": "New password"})
    confirm_new_password = PasswordField("Confirm new password", validators=[DataRequired(),
                                                                             Length(min=3, max=60),
                                                                             EqualTo("new_password", "Field must be equal to New password.")],
                                         render_kw={"placeholder": "Confirm new password"})
    submit_password = SubmitField("Update")


# ============================= ResetPasswordForm ==============================
class ResetPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),
                                            Email(),
                                            Length(min=3)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Send")
