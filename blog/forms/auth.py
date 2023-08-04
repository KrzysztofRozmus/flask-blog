from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(),
                                   Email()],
                       render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")
