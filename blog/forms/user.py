from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, EmailField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length, ValidationError
from blog.models.user import User
from blog import db


class UserForm(FlaskForm):
    username = StringField(validators=[Length(max=30)])

    email = EmailField(validators=[Length(max=30)])

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


class LogoForm(FlaskForm):
    picture = FileField(validators=[FileAllowed(["jpg", "png", "gif"])])

    submit_pic = SubmitField("Update")
