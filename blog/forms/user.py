from flask_wtf import FlaskForm
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
        user_username_in_db = db.session.execute(db.select(User).filter_by(username=username.data)).scalar()

        if username.data == "":
            pass

        elif user_username_in_db:
            raise ValidationError("That username is already taken.", "danger")

    def validate_email(self, email):
        user_email_in_db = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()

        if email.data == "":
            pass

        elif user_email_in_db:
            raise ValidationError("That email is already taken.", "danger")


class LogoForm(FlaskForm):
    picture = FileField(validators=[FileAllowed(["jpg", "png", "gif"])])

    submit_pic = SubmitField("Update")
