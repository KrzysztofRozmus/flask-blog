from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from blog.models import User
from blog import bcrypt
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
            return bcrypt.generate_password_hash(value, 14).decode("utf-8")
        return value

    def validate_username(self, username):
        usrname = User.query.filter_by(username=username.data).first()
        if usrname or username.data == "admin":
            raise ValidationError("That username is already taken.", "danger")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email is already taken.", "danger")


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(),
                                   Email()],
                       render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

    def validate_email(self, email):

        # self.user variable can be use throughout entire class.
        self.user = User.query.filter_by(email=email.data).first()
        if not self.user:
            raise ValidationError("Invalid email.", "danger")

    def validate_password(self, password):
        try:
            user = User.query.filter_by(email=self.user.email).first()
            user_password = bcrypt.check_password_hash(user.password, password.data)
            if not user_password:
                raise ValidationError("Invalid password.", "danger")

        # Handle this error if self.user.email is NoneType. It occurs if user put invalid email.
        except AttributeError:
            pass
