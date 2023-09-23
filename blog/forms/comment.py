from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired, ValidationError, data_required
from wtforms import SubmitField


class CommentForm(FlaskForm):
    content = CKEditorField(validators=[DataRequired(), InputRequired(), data_required()])
    submit = SubmitField('Submit')

    def validate_content(self, content):
        if not isinstance(content.data, str):
            raise ValidationError("This is your current username.", "danger")
