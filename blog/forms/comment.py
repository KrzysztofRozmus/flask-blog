from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class CommentForm(FlaskForm):
    content = CKEditorField(validators=[DataRequired()])
    submit = SubmitField('Submit')