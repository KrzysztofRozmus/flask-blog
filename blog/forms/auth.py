from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from blog.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from blog import db
from sqlalchemy import event


class SignupForm(FlaskForm):
    username = StringField(validators=[DataRequired(),
                                       Length(min=3, max=30)],
                           render_kw={"placeholder": "Username"})

    email = EmailField(validators=[DataRequired(),
                                   Email(),
                                   Length(min=9, max=30)],
                       render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[DataRequired(),
                                         Length(min=3, max=60)],
                             render_kw={"placeholder": "Password"})

    confirm_password = PasswordField(validators=[DataRequired(),
                                                 Length(min=3, max=60),
                                                 EqualTo("password", "Field must be equal to Password.")],
                                     render_kw={"placeholder": "Confirm password"})

    submit = SubmitField("Create account")

    # Password hash when user is created in Admin Panel.
    # hash_user_password method from: https://stackoverflow.com/a/57100627/20072823
    @event.listens_for(User.password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            # return bcrypt.generate_password_hash(value, 14).decode("utf-8")
            return generate_password_hash(value, "scrypt")
        return value

    def validate_username(self, username):
        user_username_in_db = db.session.execute(db.select(User).filter_by(username=username.data)).scalar()

        if user_username_in_db:
            raise ValidationError("That username is already taken.", "danger")

    def validate_email(self, email):
        user_email_in_db = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()

        if user_email_in_db:
            raise ValidationError("That email is already taken.", "danger")


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(),
                                   Email()],
                       render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

    def validate_email(self, email):
        # self.user_email_in_db variable can be use throughout entire class.
        self.user_email_in_db = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()

        if not self.user_email_in_db:
            raise ValidationError("Invalid email.", "danger")

    def validate_password(self, password):
        try:
            user_in_db = db.session.execute(db.select(User).filter_by(email=self.user_email_in_db.email)).scalar()
            user_password = check_password_hash(user_in_db.password, password.data)

            if not user_password:
                raise ValidationError("Invalid password.", "danger")

        # Handle this error if self.user_email_in_db.email is NoneType. It occurs if user put invalid email.
        except AttributeError:
            pass
